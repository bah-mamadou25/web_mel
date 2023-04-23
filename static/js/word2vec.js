$(document).ready(function() {
    $('#train').click(function() {
        $('#trainDiv').show();
        $('#useDiv').hide();
      })
      $('#use').click(function() {
        $('#useDiv').show();
        $('#trainDiv').hide();
      })

      $('#terme').click(function() {
        $('#termeDiv').show();
        $('#thematiqueDiv').hide();
      })
      $('#thematique').click(function() {
        $('#thematiqueDiv').show();
        $('#termeDiv').hide();
      })

  });
  