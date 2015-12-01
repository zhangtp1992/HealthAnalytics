'use strict';

describe('Service: httpHandler', function () {

  // load the service's module
  beforeEach(module('healthAnalyticsSiteApp'));

  // instantiate service
  var httpHandler;
  beforeEach(inject(function (_httpHandler_) {
    httpHandler = _httpHandler_;
  }));

  it('should do something', function () {
    expect(!!httpHandler).toBe(true);
  });

});
