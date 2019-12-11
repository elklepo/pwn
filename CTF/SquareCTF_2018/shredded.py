import PIL.Image
from pyzbar.pyzbar import decode

img_dir = r"./_shredded/"
qr_dimension = 21
brute_bucket = list()

combined_img = PIL.Image.new('RGB', ((6 + qr_dimension) * 10, 297))
blank = PIL.Image.open(img_dir + "blank.png")
combined_img.paste(blank, (0, 0))
combined_img.paste(blank, (10, 0))
combined_img.paste(blank, (20, 0))
combined_img.paste(blank, (240, 0))
combined_img.paste(blank, (250, 0))
combined_img.paste(blank, (260, 0))

images = list()
for i in range(1, qr_dimension + 1):
    images.append(PIL.Image.open(img_dir + str(i) + ".png"))

possible_positions = list()
possible_positions.append([15, 19])                 # 0
possible_positions.append([2, 3, 4])                # 1
possible_positions.append([7])                      # 2
possible_positions.append([16, 17, 18, 8, 10, 12])  # 3
possible_positions.append([0])                      # 4
possible_positions.append([1, 5])                   # 5
possible_positions.append([13])                     # 6
possible_positions.append([14, 20])                 # 7
possible_positions.append([9, 11])                  # 8
possible_positions.append([14, 20])                 # 9
possible_positions.append([1, 5])                   # 10
possible_positions.append([2, 3, 4])                # 11
possible_positions.append([15, 19])                 # 12
possible_positions.append([9, 11])                  # 13
possible_positions.append([8, 10, 12])              # 14
possible_positions.append([8, 10, 12])              # 15
possible_positions.append([16, 17, 18, 8, 10, 12])  # 16
possible_positions.append([16, 17, 18, 8, 10, 12])  # 17
possible_positions.append([16, 17, 18, 8, 10, 12])  # 18
possible_positions.append([2, 3, 4])                # 19
possible_positions.append([6])                      # 20


def get_brute(img_num, combination):
    for i in possible_positions[img_num]:
        if combination[i] == -1:
            combination[i] = img_num
            if img_num == qr_dimension - 1:
                brute_bucket.append(list(combination))
            else:
                get_brute(img_num + 1, list(combination))
                combination[i] = -1


get_brute(0, [-1] * qr_dimension)
print("Number of combinations to test - " + str(len(brute_bucket)))
n = 0
for comb in brute_bucket:
    for i in range(0, qr_dimension):
        combined_img.paste(images[comb[i]], (30 + 10 * i, 0))

    data = decode(combined_img)
    if data:
        print("Combination {}, decoded - \"{}\"".format(n, data[0].data))
        combined_img.save(img_dir + "_pwned_" + str(n) + ".png")
    n += 1
print("DONE")
