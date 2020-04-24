// Use a cacheName for cache versioning
var cacheName = 'v1:static';

// During the installation phase, you'll usually want to cache static assets.
self.addEventListener('install', function(e) {
    // Once the service worker is installed, go ahead and fetch the resources to make this work offline.
    e.waitUntil(
        caches.open(cacheName).then(function(cache) {
            return cache.addAll([
                '/',
                '/static/assets/css/core.min.css',
                '/static/assets/css/thesaas.min.css',
                '/static/assets/css/style.css',
                '/static/assets/css/custom.css',

                '/static/assets/js/core.min.js',
                '/static/assets/js/thesaas.js',
                '/static/assets/js/script.js',
                '/static/assets/js/jquery_time.min.js',

            ]).then(function() {
                self.skipWaiting();
            });
        })
    );
});

/*
self.addEventListener('fetch', function(event) {

console.log(event.request.url);

event.respondWith(

caches.match(event.request).then(function(response) {

return response || fetch(event.request);

})

);

});
*/
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - return response
        if (response) {
          return response;
        }

        // IMPORTANT: Clone the request. A request is a stream and
        // can only be consumed once. Since we are consuming this
        // once by cache and once by the browser for fetch, we need
        // to clone the response
        var fetchRequest = event.request.clone();

        return fetch(fetchRequest).then(
          function(response) {
            // Check if we received a valid response
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // IMPORTANT: Clone the response. A response is a stream
            // and because we want the browser to consume the response
            // as well as the cache consuming the response, we need
            // to clone it so we have 2 stream.
            var responseToCache = response.clone();

            caches.open(cacheName)
              .then(function(cache) {
                cache.put(event.request, responseToCache);
              });

            return response;
          }
        );
      })
    );
});
