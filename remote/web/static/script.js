document.getElementById('testme_button').onclick = sendRequest();

function sendRequest() {
    var req = new XMLHttpRequest();
    req.open('GET', localServerUrl + "?requestId=" + requestId, false);
    req.send(null);
    if (req.status == 200) {
        dump(req.responseText);
    }
    else {
        dump("error");
    }
}
