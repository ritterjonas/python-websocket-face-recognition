function People(name, image) {
    var self = this;

    self.name = ko.observable(name);
    self.image = ko.observable(image);
    self.timestamp = new Date().getTime();
}

function ViewModel() {
    var self = this;

    self.images = ko.observableArray();

    self.onMessage = function(arr) {
        self.images(ko.utils.arrayMap(arr, self.addToArray));

        self.images.sort(function (l, r) { return l.name() > r.name() ? 1 : -1 })
    }

    self.addToArray = function(item) {
        return new People(item.name, `data:image/jpg;base64,${item.image}`);
    }

    self.init = function() {
        var socket = io.connect('http://' + document.domain + ':' + location.port);

        socket.on('connect' ,function() {
            console.log('CONECTADO CHAMANDO CHECK');
            socket.emit('check', { data: 'User Connected' })
        });
        
        socket.on('image', self.onMessage);        
    }
}

var viewModel = new ViewModel();
viewModel.init();

window.onload = function() {
    ko.applyBindings(viewModel);
}
