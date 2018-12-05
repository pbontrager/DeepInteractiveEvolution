var preferrence = 0;

function outputUpdate(Preferrence) {
  preferrence = parseFloat(Preferrence / 10).toFixed(1);
  document.querySelector('#Select-Preferrence').value = preferrence;
  document.getElementById('myField').value = preferrence;
}

// function SubmitData(){
//   alert(hello);
// }
$(function() {
  $('#form1').on('submit', function(event) {
    var b = document.getElementById('btnSubmit');
    b.disabled = true;
    b.innerHTML = 'Waiting For Results...';
    // var c = document.getElementById('content');
    // c.style.display = "none";
    $('.loading_block').show();
    $('.loading_img').show();
    var pre = preferrence;
    var val = [];
      $(':checkbox:checked').each(function(i){
        val[i] = $(this).val();
      });
    var test = {"p":pre, "c":val, "id":id};
    $.ajax({
        url: '/prepare',
        data: JSON.stringify(test, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        type: 'POST',
        success: function(response) {
          b.disabled = false;
          b.innerHTML = 'Next';
          $('.loading_block').hide();
          $('.loading_img').hide();
          // alert(response);
          window.location = response
        },
        error: function(error) {
          alert(error);
        }
    });
    return false
  });
});

// window.location = response
