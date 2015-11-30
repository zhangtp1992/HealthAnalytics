angular.module('starter.config', [])
.constant('AppConfig', {
  'version': '0.1',

  /* The api server url */
  'apiUrl': 'http://www.rugatech.com/se1/api/',

  /* All apis should end in a slash '/' */
  'getUserApi': 'getUser/',
  'loginUserApi': 'loginUser/',
  'logoutUserApi': 'logoutUser/',
  'addUserApi': 'addUser/',
  'updateUserApi': 'updateUser/',
  'deleteUserApi': 'deleteUser/',

  /* Should we use local API or use the server? 'true' for local, 'false' for server */
  'apiLocal': false
  
});