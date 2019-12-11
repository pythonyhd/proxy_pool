function rot(t, u, v) {
    return String.fromCharCode(((t - u + v) % (v * 2)) + u)
}

function r13(s) {
    var b = [], c, i = s.length, a = 'a'.charCodeAt(), z = a + 26, A = 'A'.charCodeAt(), Z = A + 26;
    while (i--) {
        c = s.charCodeAt(i);
        if (c >= a && c < z) {
            b[i] = rot(c, a, 13)
        } else if (c >= A && c < Z) {
            b[i] = rot(c, A, 13)
        } else {
            b[i] = s.charAt(i)
        }
    }
    return b.join('')
}

var base64 = (function() {
var _PADCHAR = "=",
_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
_VERSION = "1.0";
function _getbyte64(s, i) {
    var idx = _ALPHA.indexOf(s.charAt(i));
    if (idx === -1) {
        throw "Cannot decode base64"
    }
    return idx
}
function _decode(s) {
    var pads = 0,
    i, b10, imax = s.length,
    x = [];
    s = String(s);
    if (imax === 0) {
        return s
    }
    if (imax % 4 !== 0) {
        throw "Cannot decode base64"
    }
    if (s.charAt(imax - 1) === _PADCHAR) {
        pads = 1;
        if (s.charAt(imax - 2) === _PADCHAR) {
            pads = 2
        }
        imax -= 4
    }
    for (i = 0; i < imax; i += 4) {
        b10 = (_getbyte64(s, i) << 18) | (_getbyte64(s, i + 1) << 12) | (_getbyte64(s, i + 2) << 6) | _getbyte64(s, i + 3);
        x.push(String.fromCharCode(b10 >> 16, (b10 >> 8) & 255, b10 & 255))
    }
    switch (pads) {
    case 1:
        b10 = (_getbyte64(s, i) << 18) | (_getbyte64(s, i + 1) << 12) | (_getbyte64(s, i + 2) << 6);
        x.push(String.fromCharCode(b10 >> 16, (b10 >> 8) & 255));
        break;
    case 2:
        b10 = (_getbyte64(s, i) << 18) | (_getbyte64(s, i + 1) << 12);
        x.push(String.fromCharCode(b10 >> 16));
        break
    }
    return x.join("")
}
function _getbyte(s, i) {
    var x = s.charCodeAt(i);
    if (x > 255) {
        throw "INVALID_CHARACTER_ERR: DOM Exception 5"
    }
    return x
}
function _encode(s) {
    if (arguments.length !== 1) {
        throw "SyntaxError: exactly one argument required"
    }
    s = String(s);
    var i, b10, x = [],
    imax = s.length - s.length % 3;
    if (s.length === 0) {
        return s
    }
    for (i = 0; i < imax; i += 3) {
        b10 = (_getbyte(s, i) << 16) | (_getbyte(s, i + 1) << 8) | _getbyte(s, i + 2);
        x.push(_ALPHA.charAt(b10 >> 18));
        x.push(_ALPHA.charAt((b10 >> 12) & 63));
        x.push(_ALPHA.charAt((b10 >> 6) & 63));
        x.push(_ALPHA.charAt(b10 & 63))
    }
    switch (s.length - imax) {
    case 1:
        b10 = _getbyte(s, i) << 16;
        x.push(_ALPHA.charAt(b10 >> 18) + _ALPHA.charAt((b10 >> 12) & 63) + _PADCHAR + _PADCHAR);
        break;
    case 2:
        b10 = (_getbyte(s, i) << 16) | (_getbyte(s, i + 1) << 8);
        x.push(_ALPHA.charAt(b10 >> 18) + _ALPHA.charAt((b10 >> 12) & 63) + _ALPHA.charAt((b10 >> 6) & 63) + _PADCHAR);
        break
    }
    return x.join("")
}
return {
    decode: _decode,
    encode: _encode,
    VERSION: _VERSION
}
} ());

function ddip(e0) {
    e1 = r13(e0.toString());
    e2 = base64.decode(e1);
    e3 = e2.toString().substr(10);
    l3 = e3.length;
    e4 = e3.substr(0, l3 - 10);
    return e4
}

// console.log(ddip('ZGH3ZwtlAGHmAwR5AP4kAQLhZwNkYwL3ZGH4ZQRmBQVmZj=='));