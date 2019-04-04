var traverson = require('traverson');
var JsonHalAdapter = require('traverson-hal');

// register the traverson-hal plug-in for media type 'application/hal+json'
traverson.registerMediaType(JsonHalAdapter.mediaType, JsonHalAdapter);

var sub_id = '5c054a529460a300074f5007'
var base_url = 'https://api.ingest.staging.data.humancellatlas.org/submissionEnvelopes/'
var sub_url = base_url + sub_id

traverson
    .from(sub_url)
    .jsonHal()
    .follow("biomaterials")
    .getResource(function(error, document) {
        if (error) {
            console.error('No luck :-)')

        } else {
            console.log('We have followed the path and reached the target resource.')
            console.log(JSON.stringify(document))
            var fs = require('fs');
            fs.writeFileSync('data.json', JSON.stringify(document));
        }

    });


// single submission envelope https://api.ingest.data.humancellatlas.org/browser/index.html#https://api.ingest.data.humancellatlas.org/submissionEnvelopes/5c054a529460a300074f5007

