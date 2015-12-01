angular.module('starter.config', [])
.constant('AppConfig', {
  'version': '0.1',

  /* The api server url */
  'apiUrl': 'http://www.rugatech.com/se1/api/',

  /* All apis should end in a slash '/' */

  // Authentication
  'loginUserApi': 'loginUser/',
  'logoutUserApi': 'logoutUser/',

  // User API
  'getUserApi': 'getUser/',
  'addUserApi': 'addUser/',
  'updateUserApi': 'updateUser/',
  'deleteUserApi': 'deleteUser/',

  // Food API
  'getFoodListApi': 'getFoodList/',
  'getFoodAllApi': 'getFoodAll/',
  'getFoodUserApi': 'getFoodUser/',
  'getFoodApi': 'getFood/',
  'addFoodApi': 'addFood/',

  // Workout API
  'getWorkoutAllApi': 'getWorkoutAll/',
  'getWorkoutUserApi': 'getWorkoutUser/',
  'getWorkoutApi': 'getWorkout/',
  'addWorkoutApi': 'addWorkout/',

  /* Should we use local API or use the server? 'true' for local, 'false' for server */
  'apiLocal': false
  
});