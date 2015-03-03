$(function(){
	$('[data-toggle="popover"]').popover({
		trigger: 'manual',
		'placement': 'right',
		container: 'body',
		'show': true
	});	
	
	$('#id_rif').keyup(function(){
		var _this = $('#id_rif');
		var _valor = $('#id_rif').val();
		var regEx = /^[JVD]-\d{8}-\d$/;
		var valid = regEx.test(_valor);
		
		if (valid){
			_this.popover('hide');
		} else {
			_this.popover('show');
		}
	});
	
});