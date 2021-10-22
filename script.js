openSocket = () => {

}

function ViewModel() {
    var self = this;

    self.images = ko.observableArray();

    self.onMessage = function(response) {
        const arr = JSON.parse(response.data);
        self.images(ko.utils.arrayMap(arr, function(e) {
            return { name: e[0], image: `data:image/jpg;base64,${e[1]}` };
        }));
    }

    self.init = function() {
        let uri = "ws://" + window.location.hostname + ":8585";
        socket = new WebSocket(uri);
        socket.addEventListener('open', (e) => {
            console.log('Opened');
        });
        socket.addEventListener('message', self.onMessage);
    }
}

var viewModel = new ViewModel();
viewModel.init();

window.onload = function() {
    ko.applyBindings(viewModel);
}
