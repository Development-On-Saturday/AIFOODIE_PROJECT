// Classifier preview image
function readURL(input) {
  if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
          $('.file-upload-image').attr('src', e.target.result);
          $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
          $('#imagePreview').hide();
          $('#imagePreview').fadeIn(650);
      };
      reader.readAsDataURL(input.files[0]);
      init().then(() => {
          console.log('hello');
          predict();
      });
  }
}
$('#imageUpload').change(function () {
  readURL(this);
});