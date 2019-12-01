## Windows Secrets #rev #forensics

### inputs 

`windows-secrets.7z` is provided with the task description, archive contains `AppData` directory.

Most interesting files are:

- `\AppData\Local\Temp\fencp.exe` - PE32 executable (console) Intel 80386, for MS Windows
- `\AppData\Local\Temp\flag.enc` - 208 raw bytes
- `\AppData\Local\Temp\BGInfo.bmp` - Wallpaper from IE 11 Win7 virtual machine that Microsoft provides for developers [here](https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/). The key observation here is that thanks to this we know the user password - `Passw0rd!`

### fencp.exe analysis

#### dynamic analysis

Running `fencp.exe` with no arguments:

> Usage: fencp.exe <file_name>

When running `fencp.exe` with path to some dummy file, nothing is printed to `stdin` or `stderr` but `flag.enc` file is created in the working directory (with different content for consecutive runs with the same input file).

*Process Monitor* shows that input file is opened, then some registry reads related to Microsoft CryptoAPI are performed. At the end `flag.enc` is created and written.

I did not spot network traffic.

#### static analysis

`fencp.exe` contains plenty of imports but a lot of crap strings suggest some kind of packing. `.text` section was almost entirely not parsed by IDA, except of one method that was most probably responsible for early stages of unpacking.

*PEid* showed that `fencp.exe` is packed with `"PEncrypt 3.1 Final -> junkcode"`. After some googling I was not able to find given packer so I decided unpack it myself. I set breakpoint at:

```
.ymz:0041C24E                 push    4018DAh
.ymz:0041C253                 retn <-------
```

After dumping process memory at this breakpoint and fixing import table I was able to get [fencp_dump.exe](./fencp_dump.exe). Loading it to IDA confirmed that I got fully unpacked binary.

#### reverse engineering

After some reverse engineering I understood the `fencp.exe` logic:

1. Open and read content (flag) from input file

2. Generate "random" key container ID in form `%08x-%04x-%04x-%02x%02x-%02x%02x%02x%02x%02x%02x` e.g. `e65e6804-f9cd-4a35-b3c9-c3a72a162e4d `

3. Open (or create if does not exist) key container for given container ID within `Microsoft Enhanced RSA and AES Cryptographic Provider` CSP

4. Load RSA key pair from key container (if it was present) or generate new RSA key pair in key container (if it was just created)

5. Generate AES-128 key

6. Encrypt file content with AES key

7. Encrypt AES key with private RSA key

8. Create `flag.enc` with content:

    ```
    offset
    0x0000 size of encrypted AES-128 key in SIMPLEBLOB format (equal to 140)
    0x0004 encrypted AES-128 key in SIMPLEBLOB format
    0x0090 encrypted file content
    ```

Above steps as they look in reversed code:

```c
// open key container
if ( !CryptAcquireContextA(
        &cspProv, 
        v_key_container_identifier, 
        "Microsoft Enhanced RSA and AES Cryptographic Provider", 
        PROV_RSA_AES, 
        0) )
{
	// create key container if does not exist
    if ( !CryptAcquireContextA(
            &cspProv,
            v_key_container_identifier,
            "Microsoft Enhanced RSA and AES Cryptographic Provider",
            PROV_RSA_AES,
            CRYPT_NEWKEYSET) )
        return -1;
  }
  
// get RSA key from keycontainer
if ( !CryptGetUserKey(cspProv, AT_KEYEXCHANGE, &rsaKey) && GetLastError() == NTE_NO_KEY )
{
	// create RSA key in key container
    if ( !CryptGenKey(cspProv, AT_KEYEXCHANGE, CRYPT_EXPORTABLE, &rsaKey) )
        return -1;
}

// generate AES-128 key
CryptGenKey(cspProv, CALG_AES_128, CRYPT_EXPORTABLE, &aesKey);

// encrpyt AES key with RSA priv key
CryptExportKey(aesKey, rsaKey, SIMPLEBLOB, 0, 0, &encAesKeyLen);
encAesKey = LocalAlloc(0x40u, encAesKeyLen);
CryptExportKey(aesKey, rsaKey, SIMPLEBLOB, 0, encAesKey, &encAesKeyLen);

// create "flag.enc"
hFile = CreateFileA("flag.enc", 0x40000000u, 0, 0, 2u, 0x80u, 0);
// write encrypted AES key size
WriteFile(hFile, &encAesKeyLen, 4u, &bytesWritten, 0);
// write encrypted AES key
WriteFile(hFile, encAesKey, encAesKeyLen, &bytesWritten, 0);
// encrpyt file content with AES key
CryptEncrypt(aesKey, 0, 1, 0, fileContent, &fileContentLen, 0x200u);
// write encrypted AES key
WriteFile(hFile, fileContent, fileContentLen, &bytesWritten, 0);

```

### solution

So we have the flag encrypted with AES key and the same AES key encrypted with RSA key stored in one of key containers. 

- Key containers are located under `\AppData\Roaming\Microsoft\Crypto\RSA\S-1-5-21-1716914095-909560446-1177810406-1000\` directory.
- User password protected master keys needed to decrypt keys in key containers are located under `C:\Users\ctfro\Desktop\ds\windows-secrets\AppData\Roaming\Microsoft\Protect\S-1-5-21-1716914095-909560446-1177810406-1000` directory.

Then I followed [this](https://github.com/gentilkiwi/mimikatz/wiki/howto-~-decrypt-EFS-files) guide on how to recover master keys (remember that we know user password) and how to decrypt keys in key containers. (In directory [extract](./extract) I've included all decrypted RSA keys from key containers).

Now all we have to do is to try to decrypt AES key with every RSA key and find the only one that will give us the correct decryption.

Last thing to do is to decrypt encrypted flag with decrypted AES key.

[exploit.py](./exploit.py) automates steps mentioned above.

> ctfzone{0h_th3s3_s3cur1ty_m3ch4n1sms_1n_w1nd0ws}

