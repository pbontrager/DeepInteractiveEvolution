var preferrence = 0;

function outputUpdate(Preferrence) {
  preferrence = parseFloat(Preferrence / 10).toFixed(1);
  document.querySelector('#Select-Preferrence').value = preferrence;
  document.getElementById('myField').value = preferrence;
}

$(function() {
  $('#form1').on('submit', function(event) {
      var b = document.getElementById('btnSubmit')
      b.disabled = true;
      b.innerHTML = 'Waiting For Results...';
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
            alert(response);
            //window.location = response
          },
          error: function(error) {
            alert("456");
          }
      });
      return false
  });
});
