$(function(){
	$('[data-toggle="popover"]').popover({
        trigger: 'manual',
        'placement': 'right',
        container: 'body',
        'show': true
    });
	
	$('#id_cedula').keyup(function(){
		var _this = $('#id_cedula');
		var _valor = $('#id_cedula').val();
		var regEx = /^([1-9][0-9]{0,3})[0-9]{0,6}$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
		
	});
	
});
