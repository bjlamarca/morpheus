'use strict'

document.querySelector('#sync-db-btn').addEventListener('click', syncHueDB)

async function syncHueDB() {
    let csrf_token = document.querySelector('#token').value;
    let url = "http://" + window.location.host + "/hue/syncdb"
    let data = []

    const request = new Request(
        url,
        { headers: { 'X-CSRFToken': csrf_token } }
      );
    
      let responce = await fetch(request, {
        method: 'POST',
        mode: 'same-origin',
        body: JSON.stringify(data) })
    
      let json = await responce.json();
    alert("Sync the DB! " + json['message'])
}