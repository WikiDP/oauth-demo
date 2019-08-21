/**
* Document ready function, loaded up on start
*/
$(document).ready( function() {
  /**
  * Event handler for submit button
  */
  $('button').click(function () {
    // Grab the data from the form object
    var formData = new FormData($('form')[0]);
    // Call the validator, with result renderer as callback
    oauthApp.login(formData, function() {
      alert("logging in");
    });
  });
});

/**
 * JavaScript wrapper JHOVE REST resources
 */
var oauthApp = {
  login : function (formData, callback, contentType = 'json') {
    $.ajax({
      url         : '/login',
      type        : 'POST',
      data        : formData,
      dataType    : contentType,
      contentType : false,
      processData : false,
      success     : function (data, textStatus, jqXHR) {
        console.log(jqXHR);
        alert(data);
        callback();
      },
      // HTTP Error handler
      error       : function (jqXHR, textStatus, errorThrown) {
        // Log full error to console
        console.log('Validation Error: ' + textStatus + errorThrown);
        console.log(jqXHR);
        // Alert the user with details
        alert('Something has gone wrong!!\n\nHTTP ' + jqXHR.status + ': ' + jqXHR.responseText);
      }
    });
  }
};
