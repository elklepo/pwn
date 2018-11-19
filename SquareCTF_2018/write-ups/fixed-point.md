# fixed point

## Description

In this task We got `fixed_point.html` that served as an interface and engine for solving this task, the flag was of course removed from this file. We also had access to `fixed_point.html` hosted in remote server to obtain the real flag one We find out how to do this in local environment.

The code was very simple:

```js
function f(x) {
  if ((x.substr(0, 2) == '🚀') && (x.slice(-2) == '🚀')) {
    return x.slice(2, -2);
  }
  if (x.substr(0, 2) == '👽') {
    return '🚀' + f(x.slice(2));
  }
  if (x.substr(0, 2) == '📡') {
    return f(x.slice(2)).match(/..|/g).reverse().join("");
  }
  if (x.substr(0, 2) == '🌗') {
    return f(x.slice(2)).repeat(5);
  }
  if (x.substr(0, 2) == '🌓') {
    var t = f(x.slice(2));
    return t.substr(0, t.length/2);
  }
  return "";
}
```

The rest of `fixed_point.html` was responsible for collecting input and validating it. Below is the condition that had to be met to obtain the flag:

```js
function check() {
  var i = input.value.replace(/\s/g, '');
  if (i == "") {
    result.innerText = "";
  } else {
    var t = f(i);
    if (t == i) {
      result.innerText = "good!"; //flag on remote server
    } else {
      result.innerText = "bad! (" + t + " != " + i + ")";
    }
  }
}
```

As We can see, the condition is also very simple  `input == f(input)`.

## Solution

The first thing I did was rewrite this code to Python and brute force it, I've managed to test all combinations on input with length $\langle1; 12\rangle$ but it finished with no solution, the input must've been longer so I've started manual input construction. After some time, I approached the strategy, which can be shortened to the following bullets:

* The right side of the input is constructed in form - 🚀...`payload`...🚀. The output will be constructed only form `payload` elements.
* The left side of the input is combination of 🌓 and 🌗 (lets call it `header`). By changing the number and positions of those two moons I was able to change the length and the structure of output which was constructed from `payload`.
* Number of 📡 are added in `header`, somewhere between 🌓 and 🌗. The point of this is to manipulate the structure of output, and to change the length of input without changing the length of the output.
* The length of the `payload` must be the multiple of `header` length incremented by one. This concept allowed to easily match the two 🚀that surround the `payload`  (both  🚀 were covered in output by the same element form multiplied `payload`).

After defining this strategy in my mind I Was finally able to find the valid input:

🌓📡📡📡🌓🌗🚀🚀👽👽👽👽👽👽👽🚀🚀🌗🌓📡📡📡🌓👽👽👽👽👽👽👽👽👽🌓📡📡📡🌓🌗🚀🚀

> good! flag-2d4584368d09da2187f5
