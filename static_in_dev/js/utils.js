$(document).ready(function(){

	$('.remove-from-cart').on('click', function(e){
		e.preventDefault();
		product_slug = $(this).attr('data-slug');
		item_cart_id = $(this).attr('data-id');
		data = {
			product_slug: product_slug
		}
		$.ajax({
			type: "GET",
			url: "{% url 'remove_from_cart_view' %}",
			data: data,
			success: function(data){
				$('#cart-count').html(data.total);
				$('.cart-item-'+item_cart_id).css('display', 'none');
			}
		});
	});

	$('.add-to-cart').on('click', function(e){
		e.preventDefault();
		product_slug = $(this).attr('data-slug');
		data = {
			product_slug: product_slug
		}
		$.ajax({
			type: "GET",
			url: "{% url 'add_to_cart_view' %}",
			data: data,
			success: function(data){
				$('#cart-count').html(data.total)
			}
		});
	});

});