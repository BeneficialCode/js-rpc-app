const CryptoJS = require('crypto-js');
window = {}

const JSEncrypt = require('jsencrypt');

var KSTR = "";
var AESPK = "";
var AESIV = "";
createK();
var RSAPK = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQClAacOJd7wQ8snEM+nRS2W" +
    "d2Cuyt9d+Igu216Xb+E+e2M7d5tAaVnIGpsOgydo0SgLjIqgZeoXpWvXh7BR" +
    "mFbxAA0w6FTQ4Xbr+cAetNSJ6WfSTprBGl0LOM/YUhmcUs4WqW5lbCl1kNE1" +
    "1IP18eVKyCmpjShHA5PMHgNXLUNVQQIDAQAB";


//生成AES的key和偏移量
function createK(){
    var kStr = generateRandomString(64);
    KSTR = kStr;
    AESPK = substringFromString(kStr,6,32);
    AESIV = substringFromString(kStr,30,16);
}

function generateK(kStr){
    KSTR = kStr;
    AESPK = substringFromString(kStr,6,32);
    AESIV = substringFromString(kStr,30,16);
}

//截取字符串
function substringFromString(originalString, startPosition, length) {
    // 检查输入是否有效
    if (typeof originalString !== 'string' || typeof startPosition !== 'number' || typeof length !== 'number') {
        throw new Error('Invalid input');
    }
    // 检查开始位置和长度是否在字符串的有效范围内
    if (startPosition < 0 || startPosition >= originalString.length || length < 0 || startPosition + length > originalString.length) {
        throw new Error('Start position or length is out of range');
    }
    // 使用substring()方法截取字符串
    return originalString.substring(startPosition, startPosition + length);
}

/** 判断对象是否为空 **/
function isEmpty(object){
    if(object==null){
        return true;
    }
    if(object==''){
        return true;
    }
    if(object==undefined){
        return true;
    }
    if(object=='undefined'){
        return true;
    }
    return false;
}

//随机字符串生成
function generateRandomString(length) {
    let result = 'Wf4WCa1IcTojhrAsAWgmNoENowGBCcxvira2NWpmdmYh3eSPu3JqcicRuacwv8IC';
    // const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    // const charactersLength = characters.length;
    // for (let i = 0; i < length; i++) {
    //     result += characters.charAt(Math.floor(Math.random() * charactersLength));
    // }
    return result;
}
// AES加密函数
function encryptAES(plaintext) {
    const keyHex = CryptoJS.enc.Utf8.parse(AESPK);
    const ivHex = CryptoJS.enc.Utf8.parse(AESIV);
    const encrypted = CryptoJS.AES.encrypt(plaintext, keyHex, {
        iv: ivHex,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return encrypted.toString();
}

// AES解密函数
function decryptAES(ciphertext) {
    const keyHex = CryptoJS.enc.Utf8.parse(AESPK);
    const ivHex = CryptoJS.enc.Utf8.parse(AESIV);
    const decrypted = CryptoJS.AES.decrypt(ciphertext, keyHex, {
        iv: ivHex,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return decrypted.toString(CryptoJS.enc.Utf8);
}

// RSA加密
function encryptRSA(content) {
    const encryptor = new JSEncrypt();
    encryptor.setPublicKey(RSAPK);
    //生成时间戳
    var kestr = content+','+new Date().getTime();
    return encryptor.encrypt(kestr); // 对数据进行加密
}

function get_kestr(){
    var kestr = encryptRSA(KSTR);
    console.log(kestr);
    return kestr;
}

function get_kstr(){
    return KSTR;
}

function get_req_cookie(data) 
{
    // 17381560710$$201$地市（中文/拼音）$23$$$0
    var val = ''
    var crypto_key = "login.189.cn";
    val = CryptoJS.AES.encrypt(data, crypto_key);
    return val.toString();
}


module.exports = {
    decryptAES,
    generateK,
    encryptRSA,
    get_kestr,
    encryptAES,
    get_req_cookie,
}