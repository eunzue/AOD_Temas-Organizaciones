/*** Aquí tenemoes las funciones necesarias para hacer la web Responsive ***/
function responsiveScroll() {
	$(window).scroll(function() {
		if ($(window).width()>=1012){
			$html = $("html");
			$('.mini .botones').css('top','35px');
			//Esto se debe de modificar ya que todos los navegadores lo pueden hacer de modo diferente
			/*if($html.hasClass('webkit')){
				var scrollTop = $("body")[0].scrollTop;
			}else if($html.hasClass('firefox')){
				var scrollTop = $("html")[0].scrollTop;
			}else{
				var scrollTop = $(document).scrollTop();
			
				//var scrollTop = $("body")[0].scrollTop;
				//var scrollTop = $("html")[0].scrollTop;
			}*/

		
			//Con window creo que pilla La barra de scroll ya que el lÃ­mite esta en 754 con lo que esta barra tiene 14 pixeles
			//if (($( window ).width()>754) && ($(document).scrollTop() >= 160)){
			if ($(document).scrollTop() >= 150){
				$('body').addClass('mini');
				//$('#anchoBanner').css('top', $(document).scrollTop()+'px');
				$('#anchoBanner').css({
					'position':'fixed',
					'top': '-10px',
					'height':$('.banner').height(),
					'width':'100%',
					'z-index':1110
				});
				$('.banner').css('left', (($(window).width()-$('.banner').width())/2)+'px');
			}
			else{
				$('body').removeClass('mini');
				$('.banner').removeAttr('style');
				$('#anchoBanner').removeAttr('style');
				$('#anchoBanner').css('background-color', '#76a1b8');
				if ($(document).scrollTop() >= 150){
					//alert('borrar el style del banner');
					$('.banner').removeAttr('style');
				}
			}
			/*if( scrollTop < 160 ){
				$('body').removeClass('mini');
			}else{
				$('body').addClass('mini');
			}*/
		}
		else{
			$('.mini .botones').removeAttr('style');
			$('.banner').removeAttr('style');
		}
	});
	$("body").trigger('scroll');
}
//});

function refinaAutocomplete() {
	$.ui.autocomplete.prototype._renderItem = function( ul, item) {
		return $( "<li></li>" )
			.data( "item.autocomplete", item )
			.append( "<a href='http://opendata.aragon.es/catalogo/" + item.valor + "'>" + item.label + "</a>" )
			.appendTo( ul );
	};	
}




// cookies function from http://www.w3schools.com/js/js_cookies.asp
function getCookie(cname) {
	var name = cname + "=";
	var ca = document.cookie.split(';');
	for(var i=0; i<ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1);
		if (c.indexOf(name) == 0) return c.substring(name.length,c.length);
	}
	return "";
}


function isEmpty(value){
	return (value == null || value === '');
}
//Esta funcion pinta el menu de buscador según si esta usuario logueado o no
function pintaMenuBuscador(){
	var login=getCookie('auth_tkt');
	//Borramos el menu para pintarlo según el resultado de la cookien que contiene si estamos logueados
	$(".bannerBuscador").empty();
	if (isEmpty(login)){
		//Pintamos el menu para loguearse
		$(".bannerBuscador").append('<form id="cajaBusqBanner" action="http://opendata.aragon.es/catalogo" method="get"><span role="status" aria-live="polite" class="ui-helper-hidden-accessible"></span><input id="cajaDeBusqInput" name="q" value="" class="search anchoSearchBanner cajaDeBusqInput ui-autocomplete-input" type="text" autocomplete="off"><button class="btn-search" type="submit">Buscar</button><a href="http://opendata.aragon.es/catalogo/user/login" title="Iniciar Sesión"><img src="http://opendata.aragon.es/public/i/login.jpg" alt="Iniciar Sesión" class="btn-login"></a></form>');
	}
	else{
		//Pintamos el menu cuando estamos logueados
		$(".bannerBuscador").append('<form id="cajaBusqBanner" action="http://opendata.aragon.es/catalogo" method="get"><span role="status" aria-live="polite" class="ui-helper-hidden-accessible"></span><input id="cajaDeBusqInput" name="q" value="" class="search anchoSearchBanner cajaDeBusqInput ui-autocomplete-input" type="text" autocomplete="off"><a href="http://opendata.aragon.es/catalogo/pizarra" title="Pizarra de administración"><img src="http://opendata.aragon.es/public/i/dashboard.jpg" alt="Pizarra de administración" class="btn-login"></a><a href="http://opendata.aragon.es/catalogo/user/_logout" title="Salir"><img src="http://opendata.aragon.es/public/i/logout.jpg" alt="Salir" class="btn-login"></a></form>');
	}
	if ($(window).width()>1024){
		//Este div se usa para que quede centrado
		$('<div id="anchoBanner" style="background-color: #76a1b8;"></div>').insertBefore('.banner');
		$('.banner').appendTo('#anchoBanner');
		//Borramos los #anchoBanner internos que nos guarrean el codigo si andamos agrandando o empequeñeciendo la ventana
		$('#anchoBanner #anchoBanner').remove();
	}
}

function responsiveWebErrores(){
	var anchoVideo = $('.seccionHome').width();
	var altoVideo = $('.seccionHome').width() *315/560;
	$('#errores iframe').css('width', anchoVideo+'px');
	$('#errores iframe').css('height', altoVideo+'px');
}



$(document).ready(function() {
	pintaMenuBuscador();
	responsiveScroll();
	responsiveWebErrores();
	
	$(window).resize(function() {
		pintaMenuBuscador();
		responsiveScroll();
		responsiveWebErrores();
	});
	
});
