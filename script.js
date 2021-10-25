openSocket = () => {

}

function People(name, image) {
    var self = this;

    self.name = ko.observable(name);
    self.image = ko.observable(image);
    self.timestamp = new Date().getTime();
}

function ViewModel() {
    var self = this;

    self.images = ko.observableArray();

    self.onMessage = function(response) {
        const arr = JSON.parse(response.data);
        
        self.images(ko.utils.arrayMap(arr, self.addToArray));

        self.images.sort(function (l, r) { return l.name() > r.name() ? 1 : -1 })
    }

    self.addToArray = function(item) {
        return new People(item[0], `data:image/jpg;base64,${item[1]}`);
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
