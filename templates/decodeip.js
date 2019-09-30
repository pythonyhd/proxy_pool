

function decode(str) {
    return (str + '').replace(/[a-z]/gi, function(s) {return String.fromCharCode(s.charCodeAt(0) + (s.toLowerCase() < 'n' ? 13 : -13));});
};


// console.log(decode('AwNhZwN1YwR1BF4kBGH='))