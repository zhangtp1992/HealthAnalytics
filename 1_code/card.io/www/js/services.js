angular.module('starter.services', [])
.factory('UserService', function($timeout, $filter, $q) {
  var service = {};
  service.GetAll = GetAll;
  service.GetById = GetById;
  service.GetByUsername = GetByUsername;
  service.Create = Create;
  service.Update = Update;
  service.Delete = Delete;
  return service;

  function GetAll() {
    var deferred = $q.defer();
    deferred.resolve(getUsers());
    return deferred.promise;
  }

  function GetById(id) {
    var deferred = $q.defer();
    var filtered = $filter('filter')(getUsers(), { id: id });
    var user = filtered.length ? filtered[0] : null;
    deferred.resolve(user);
    return deferred.promise;
  }

  function GetByUsername(username) {
    var deferred = $q.defer();
    var filtered = $filter('filter')(getUsers(), { username: username });
    var user = filtered.length ? filtered[0] : null;
    deferred.resolve(user);
    return deferred.promise;
  }

  function Create(user) {
    var deferred = $q.defer();
    $timeout(function () {
      GetByUsername(user.username)
      .then(function (duplicateUser) {
        if (duplicateUser !== null) {
          deferred.resolve({ success: false, message: 'Username "' + user.username + '" is already taken' });
        } else {
          var users = getUsers();

          var lastUser = users[users.length - 1] || { id: 0 };
          user.id = lastUser.id + 1;

          users.push(user);
          setUsers(users);

          deferred.resolve({ success: true });
        }
      });
    }, 1000);
    return deferred.promise;
  }

  function Update(user) {
    var deferred = $q.defer();
    var users = getUsers();
    for (var i = 0; i < users.length; i++) {
      if (users[i].id === user.id) {
        users[i] = user;
        break;
      }
    }
    setUsers(users);
    deferred.resolve();
    return deferred.promise;
  }

  function Delete(id) {
    var deferred = $q.defer();
    var users = getUsers();
    for (var i = 0; i < users.length; i++) {
      var user = users[i];
      if (user.id === id) {
        users.splice(i, 1);
        break;
      }
    }
    setUsers(users);
    deferred.resolve();
    return deferred.promise;
  }

  function getUsers() {
    if(!localStorage.users){
      localStorage.users = JSON.stringify([]);
    }

    return JSON.parse(localStorage.users);
  }

  function setUsers(users) {
    localStorage.users = JSON.stringify(users);
  }
})

.factory('AuthenticationService', function($http, $cookieStore, $rootScope, $timeout, UserService){
  var service = {};
  service.Login = Login;
  service.SetCredentials = SetCredentials;
  service.ClearCredentials = ClearCredentials;
  service.IsLoggedIn = IsLoggedIn;
  service.CurrentUser = CurrentUser;
  return service;

  function Login(username, password, callback) {
    /* Dummy authentication for testing, uses $timeout to simulate api call */
    $timeout(function () {
      var response;
      UserService.GetByUsername(username)
      .then(function (user) {
        if (user !== null && user.password === password) {
          response = { success: true, user: user };
        } else {
          response = { success: false, message: 'Username or password is incorrect'};
        }
        callback(response);
      });
    }, 1000);
    /* Use this for real authentication
    $http.post('/api/authenticate', { username: username, password: password })
    .success(function (response) {
      callback(response);
    });
    */
  }

  function SetCredentials(username, password, user) {
    var authdata = Base64.encode(username + ':' + password);
    $rootScope.globals = {
      currentUser: {
        username: username,
        authdata: authdata,
        user: user
      }
    };
    $http.defaults.headers.common['Authorization'] = 'Basic ' + authdata; // jshint ignore:line
    $cookieStore.put('globals', $rootScope.globals);
  }

  function CurrentUser(){
    if($rootScope.globals.currentUser){
      return $rootScope.globals.currentUser.user;
    } else {
      return {};
    }
     
  }

  function IsLoggedIn(){
    if($rootScope.globals.currentUser){
      return true;
    } else {
      return false;
    }
  }

  function ClearCredentials() {
    $rootScope.globals = {};
    $cookieStore.remove('globals');
    $http.defaults.headers.common.Authorization = 'Basic ';
  }
})

.factory('FlashService', function($rootScope){
  var service = {};
  service.Success = Success;
  service.Error = Error;
  initService();
  return service;

  function initService() {
    $rootScope.$on('$locationChangeStart', function () {
      clearFlashMessage();
    });

    function clearFlashMessage() {
      var flash = $rootScope.flash;
      if (flash) {
        if (!flash.keepAfterLocationChange) {
          delete $rootScope.flash;
        } else {
          flash.keepAfterLocationChange = false;
        }
      }
    }
  }

  function Success(message, keepAfterLocationChange) {
    $rootScope.flash = {
      message: message,
      type: 'success', 
      keepAfterLocationChange: keepAfterLocationChange
    };
  }

  function Error(message, keepAfterLocationChange) {
    $rootScope.flash = {
      message: message,
      type: 'error',
      keepAfterLocationChange: keepAfterLocationChange
    };
  }
});

/*
.factory('UserService', function($http) {
  var service = {};
  service.GetAll = GetAll;
  service.GetById = GetById;
  service.GetByUsername = GetByUsername;
  service.Create = Create;
  service.Update = Update;
  service.Delete = Delete;
  return service;

  function GetAll() {
    return $http.get('/api/users').then(handleSuccess, handleError('Error getting all users'));
  }

  function GetById(id) {
    return $http.get('/api/users/' + id).then(handleSuccess, handleError('Error getting user by id'));
  }

  function GetByUsername(username) {
    return $http.get('/api/users/' + username).then(handleSuccess, handleError('Error getting user by username'));
  }

  function Create(user) {
    return $http.post('/api/users', user).then(handleSuccess, handleError('Error creating user'));
  }

  function Update(user) {
    return $http.put('/api/users/' + user.id, user).then(handleSuccess, handleError('Error updating user'));
  }

  function Delete(id) {
    return $http.delete('/api/users/' + id).then(handleSuccess, handleError('Error deleting user'));
  }

  function handleSuccess(res) {
    return res.data;
  }

  function handleError(error) {
    return function () {
      return { success: false, message: error };
    };
  }
})
*/



// Base64 encoding service used by AuthenticationService
var Base64 = {

  keyStr: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=',

  encode: function (input) {
    var output = "";
    var chr1, chr2, chr3 = "";
    var enc1, enc2, enc3, enc4 = "";
    var i = 0;

    do {
      chr1 = input.charCodeAt(i++);
      chr2 = input.charCodeAt(i++);
      chr3 = input.charCodeAt(i++);

      enc1 = chr1 >> 2;
      enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
      enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
      enc4 = chr3 & 63;

      if (isNaN(chr2)) {
        enc3 = enc4 = 64;
      } else if (isNaN(chr3)) {
        enc4 = 64;
      }

      output = output +
      this.keyStr.charAt(enc1) +
      this.keyStr.charAt(enc2) +
      this.keyStr.charAt(enc3) +
      this.keyStr.charAt(enc4);
      chr1 = chr2 = chr3 = "";
      enc1 = enc2 = enc3 = enc4 = "";
    } while (i < input.length);

    return output;
  },

  decode: function (input) {
    var output = "";
    var chr1, chr2, chr3 = "";
    var enc1, enc2, enc3, enc4 = "";
    var i = 0;

    // remove all characters that are not A-Z, a-z, 0-9, +, /, or =
    var base64test = /[^A-Za-z0-9\+\/\=]/g; 
    if (base64test.exec(input)) {
      window.alert("There were invalid base64 characters in the input text.\n" +
        "Valid base64 characters are A-Z, a-z, 0-9, '+', '/',and '='\n" +
        "Expect errors in decoding.");
    }
    input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

    do {
      enc1 = this.keyStr.indexOf(input.charAt(i++));
      enc2 = this.keyStr.indexOf(input.charAt(i++));
      enc3 = this.keyStr.indexOf(input.charAt(i++));
      enc4 = this.keyStr.indexOf(input.charAt(i++));

      chr1 = (enc1 << 2) | (enc2 >> 4);
      chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
      chr3 = ((enc3 & 3) << 6) | enc4;

      output = output + String.fromCharCode(chr1);

      if (enc3 != 64) {
        output = output + String.fromCharCode(chr2);
      }
      if (enc4 != 64) {
        output = output + String.fromCharCode(chr3);
      }

      chr1 = chr2 = chr3 = "";
      enc1 = enc2 = enc3 = enc4 = "";

    } while (i < input.length);

    return output;
  }
};