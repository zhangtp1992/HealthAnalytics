angular.module('starter.services', ['starter.config'])
.factory('UserService', function($http, AppConfig) {
  var service = {};
  if(AppConfig.apiLocal) { // If the API is set to local, user the Local functions
    service.GetAll = GetAllLocal;
    service.GetById = GetByIdLocal;
    service.GetByUsername = GetByUsernameLocal;
    service.Create = CreateLocal;
    service.Update = UpdateLocal;
    service.Delete = DeleteLocal;
  } else { // else use the actual API functions.
    service.GetAll = GetAll;
    service.GetById = GetById;
    service.GetByUsername = GetByUsername;
    service.Create = Create;
    service.Update = Update;
    service.Delete = Delete;
  }
  return service;

  // API Service Functions
  function GetAll() {
    return $http.get(AppConfig.apiUrl + AppConfig.getUserApi).then(handleSuccess, handleError);
  }

  function GetById(id) {
    return $http.get(AppConfig.apiUrl + AppConfig.getUserApi + id).then(handleSuccess, handleError);
  }

  function GetByUsername(username) {
    return $http.get(AppConfig.apiUrl + AppConfig.getUserApi + username).then(handleSuccess, handleError);
  }

  function Create(user) {
    return $http.post(AppConfig.apiUrl + AppConfig.addUserApi + user.username, user).then(handleSuccess, handleError);
  }

  function Update(user) {
    return $http.put(AppConfig.apiUrl + AppConfig.updateUserApi + user.username, user).then(handleSuccess, handleError);
  }

  function Delete(id) {
    return $http.delete(AppConfig.apiUrl + AppConfig.deleteUserApi + username).then(handleSuccess, handleError);
  }

  function handleSuccess(response) {
    return { success:true, code:response.status, data: response.data };
  }

  function handleError(response) {
    return { success: false, code:response.status , data: response.statusText };
  }

  // Local Service Functions
  function GetAllLocal() {
    var deferred = $q.defer();
    deferred.resolve(getUsers());
    return deferred.promise;
  }

  function GetByIdLocal(id) {
    var deferred = $q.defer();
    var filtered = $filter('filter')(getUsers(), { id: id });
    var user = filtered.length ? filtered[0] : null;
    deferred.resolve(user);
    return deferred.promise;
  }

  function GetByUsernameLocal(username) {
    var deferred = $q.defer();
    var filtered = $filter('filter')(getUsers(), { username: username });
    var user = filtered.length ? filtered[0] : null;
    deferred.resolve(user);
    return deferred.promise;
  }

  function CreateLocal(user) {
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
          user.authtoken = 'sometoken';

          users.push(user);
          setUsers(users);

          deferred.resolve({ success: true });
        }
      });
    }, 1000);
    return deferred.promise;
  }

  function UpdateLocal(user) {
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

  function DeleteLocal(id) {
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

.factory('AuthenticationService', function($http, $cookieStore, $rootScope, $timeout, UserService, AppConfig){
  var service = {};
  service.Login = Login;
  service.Logout = Logout;
  service.SetCredentials = SetCredentials;
  service.ClearCredentials = ClearCredentials;
  service.IsLoggedIn = IsLoggedIn;
  service.CurrentUser = CurrentUser;
  return service;

  function Login(username, password, callback) {

    /* If our config points to 'Local' we use dummy authentication for testing, uses $timeout to simulate api call */
    if(AppConfig.apiLocal) {
      $timeout(function () {
        var response;
        UserService.GetByUsername(username)
        .then(function (user) {
          if (user !== null && user.password === password) {
            SetCredentials(username, password, user.token);
            response = { success: true, code:200 , data: 'Ok' };
          } else {
            response = { success: false, code:401 , data: 'Username or password is incorrect'};
          }
          callback(response);
        });
      }, 1000);
    } else { /* Else, use real API Authentication */
      $http.post(AppConfig.apiUrl + AppConfig.loginUserApi + username, { password: password })
      .then(function (resp) { // success
        var token = resp.data;
        if(token && token.authtoken){
          // we logged in, let's retrieve the user
          SetCredentials(username, password, token.authtoken, undefined);
          UserService.GetByUsername(username.toLowerCase())
          .then(function(response) {
            if(response.success) {
              SetCredentials(username, password, token.authtoken, response.data);
            } else {
              Logout(); // logout because we couldn't retrieve the user...
            }
            callback(response); // send response, this covers both OK and BAD
          });
        }
      }, function (resp){ // error
        var response = { success: false, code: resp.status, data: resp.statusText };
        callback(response);
      });
    }
  }

  function SetCredentials(username, password, token, user) {
    $rootScope.globals = {
      currentUser: {
        username: username,
        password: password,
        authdata: token,
        user: user
      }
    };
    // Setting the authentication token/credentials for all http requests
    $http.defaults.headers.common['AuthToken'] = token;
    $cookieStore.put('globals', $rootScope.globals);
  }

  function CurrentUser(){
    if($rootScope.globals.currentUser){
      return $rootScope.globals.currentUser;
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

  function Logout() {
    var user = CurrentUser();
    if (user && user.username) {
      $http.post(AppConfig.apiUrl + AppConfig.logoutUserApi + user.username)
      .then(function (response) { // success
        ClearCredentials(); // Success or fail, we will clear credentials anyway....
      }, function (response) { // error
        ClearCredentials(); // Success or fail, we will clear credentials anyway....
      });
    } else {
      ClearCredentials(); // Success or fail, we will clear credentials anyway....
    }
    
  }

  function ClearCredentials() {
    $rootScope.globals = {};
    $cookieStore.remove('globals');
    // Clearing the authentication token/credentials for all http requests
    $http.defaults.headers.common['AuthToken'] = undefined;
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