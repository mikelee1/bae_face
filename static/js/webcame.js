'use strict';
var constraints = {
  video: true,
  audio:true
};
var video = document.querySelector('video');
var video1 = document.getElementById('p');
function handleSuccess(stream) {
  window.stream = stream; // only to make stream available to console
//  video.srcObject = stream;
    if ("srcObject" in video) {
            video.srcObject = stream
        } else {
            video.src = window.URL && window.URL.createObjectURL(stream) || stream
        }
  video1.innerHTML = 'aaa';
}
function handleError(error) {
  console.log('getUserMedia error: ', error);
  video1.innerHTML = 'bbb';
  alert("error!");
if (error.PERMISSION_DENIED) {
alert('用户拒绝了浏览器请求媒体的权限');
} else if (error.NOT_SUPPORTED_ERROR) {
alert('对不起，您的浏览器不支持拍照功能，请使用其他浏览器');
} else if (error.MANDATORY_UNSATISFIED_ERROR) {
alert('指定的媒体类型未接收到媒体流');
} else {
alert('系统未能获取到摄像头，请确保摄像头已正确安装。或尝试刷新页面，重试');
}
}
navigator.mediaDevices.getUserMedia(constraints).
  then(handleSuccess).catch(handleError);


