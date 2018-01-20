var firebaseuiPage = {
    fields: { email: "", password: "" },
    setFields: function() {
        $("[name='username']").val(firebaseuiPage.email);
        $("[name='password']").val(firebaseuiPage.password);
    },
    resetFields: function() {
        firebaseuiPage.fields = { email: "", password: "" };
        firebaseuiPage.setFields();
    },
    validator: function() {
        isValid = true;

        return isValid;
    },
    config: { "get from firebase web setup" },
    services: {},
    providers: { google: new firebase.auth.GoogleAuthProvider().addScope('https://www.googleapis.com/auth/plus.login'), facebook: new firebase.auth.FacebookAuthProvider().addScope('user_birthday'), twitter: new firebase.auth.TwitterAuthProvider() },
    events: {
        createUserWithEmailAndPassword: function() {
            firebaseuiPage.services.auth.createUserWithEmailAndPassword(firebaseuiPage.fields.email, firebaseuiPage.fields.password).then(function(resp) {
                console.log(resp);
                firebaseuiPage.resetFields();
            }).catch(function(err) {
                console.log(err);
            });
        },
        signInWithEmailAndPassword: function() {
            firebaseuiPage.services.auth.signInWithEmailAndPassword(firebaseuiPage.fields.email, firebaseuiPage.fields.password).then(function(resp) {
                console.log(resp);
                firebaseuiPage.resetFields();
            }).catch(function(err) {
                console.log(err);
            });
        },
        signInWithPopup: function(provider) {
            firebaseuiPage.services.auth.signInWithPopup(provider).then(function(resp) {
                console.log(resp);
            }).catch(function(err) {
                console.log(err);
            });
        },
        onAuthStateChanged: function() {
            firebaseuiPage.services.auth.onAuthStateChanged(function(user) {
                if (user) {
                    // User is signed in.
                } else {
                    // No user is signed in.
                }
            });
        },
        signOut: function() { firebaseuiPage.services.auth.signOut(); }
    }
};

$(document).ready(function() {
    firebase.initializeApp(firebaseuiPage.config);
    firebaseuiPage.services.auth = firebase.auth();
    firebaseuiPage.services.messaging = firebase.messaging();
    firebaseuiPage.events.onAuthStateChanged();
    firebaseuiPage.services.messaging.requestPermission().then(function() {
        alert("messaging permission granted");
        return firebaseuiPage.services.messaging.getToken();
    }).then(function(token) {
        console.log(token);
    }).catch(function(err) {
        alert("messaging permission denied");
    });
    $("[name='btn_sign_up']").on('click', function() { firebaseuiPage.events.createUserWithEmailAndPassword(); });
    $("[name='btn_sign_in']").on('click', function() { firebaseuiPage.events.signInWithEmailAndPassword(); });
    $("[name='btn_sign_fb']").on('click', function() { firebaseuiPage.events.signInWithPopup(firebaseuiPage.providers.facebook); });
    $("[name='btn_sign_gp']").on('click', function() { firebaseuiPage.events.signInWithPopup(firebaseuiPage.providers.google); });
    $("[name='btn_sign_tw']").on('click', function() { firebaseuiPage.events.signInWithPopup(firebaseuiPage.providers.twitter); });
    $("[name='btn_sign_out']").on('click', function() { firebaseuiPage.events.signOut(); });

});