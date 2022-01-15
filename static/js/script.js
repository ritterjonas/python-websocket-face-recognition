function ViewModel() {
  var self = this;

  self.people = ko.observableArray();

  self.proccess = function () {
    var canvas = document.createElement("canvas");
    canvas.height = video.videoHeight;
    canvas.width = video.videoWidth;
    var context = canvas.getContext("2d");
    context.drawImage(video, 0, 0);
    canvas.toBlob(
      function (blob) {
        if (!blob) {
          self.proccess();
          return;
        }

        const formData = new FormData();
        formData.append("file", blob, "filename.jpg");

        $.ajax({
          url: "/detect",
          data: formData,
          processData: false,
          contentType: false,
          type: "POST",
          success: function (data) {
            self.people(data);
          },
          complete: function () {
            self.proccess();
          },
        });
      },
      "image/jpeg",
      0.95
    );
  };
}

var viewModel = new ViewModel();

$(function () {
  navigator.mediaDevices
    .getUserMedia({
      video: {
        width: { ideal: 1080 },
        height: { ideal: 720 },
        // deviceId: {
        //   exact:
        //     "ff9225ebf76c197e41c2d3e35b8039edc9d063c0e0309d902e37834e6bfc9e77",
        // },
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
