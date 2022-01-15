function ViewModel() {
  var self = this;

  self.init = function () {};

  self.proccess = function () {
    var canvas = document.createElement("canvas");
    canvas.height = video.videoHeight;
    canvas.width = video.videoWidth;
    var context = canvas.getContext("2d");
    context.drawImage(video, 0, 0);
    canvas.toBlob(function (blob) {
      if (!blob) {
        self.proccess();
        return;
      }

      const formData = new FormData();
      formData.append("file", blob, "filename.png");

      $.ajax({
        url: "/detect",
        data: formData,
        processData: false,
        contentType: false,
        type: "POST",
        success: function (data) {
          console.log(data);
        },
        complete: function () {
          self.proccess();
        },
      });
    });
  };
}

var viewModel = new ViewModel();

$(function () {
  navigator.mediaDevices
    .getUserMedia({
      video: {
        deviceId: {
          exact:
            "ff9225ebf76c197e41c2d3e35b8039edc9d063c0e0309d902e37834e6bfc9e77",
        },
      },
    })
    .then(function (mediaStream) {
      var video = document.querySelector("#video");

      video.srcObject = mediaStream;
      video.play();
      viewModel.proccess();
    })
    .catch(function (err) {
      console.log("Não há permissões para acessar a webcam");
    });

  ko.applyBindings(viewModel);
});
