let source = new EventSource("/stream");

source.addEventListener("message", function(event) {
    let data = JSON.parse(event.data);
    alert(data.message);
}, false);

source.addEventListener("error", function(event) {
    console.error("Failed to connect to event stream. Is the server running?");
}, false);