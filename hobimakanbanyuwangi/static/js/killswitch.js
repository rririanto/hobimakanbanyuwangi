    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.getRegistrations().then(function(registrations) {
            for (var registration of registrations) {
                registration.unregister();
            }
        });
    }
