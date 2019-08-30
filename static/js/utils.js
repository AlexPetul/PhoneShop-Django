$(document).ready(function(){

  $('.empty-cart-inv').css('display', 'none');

  $('.add-to-cart').on('click', function(e){
    e.preventDefault();
    product_slug = $(this).attr('data-slug');
    data = {
      product_slug: product_slug
    }
    $.ajax({
      type: "GET",
      url: url_add_to_cart,
      data: data,
      success: function(data){
        $('#cart-count').html(data.total)
      }
    });
  });

  $('.remove-from-cart').on('click', function(e){
    e.preventDefault();
    product_slug = $(this).attr('data-slug');
    item_id = $(this).attr('data-item-id');
    data = {
      product_slug: product_slug
    }
    $.ajax({
      type: "GET",
      url: url_remove_from_cart,
      data: data,
      success: function(data){
        $('#cart-count').html(data.total);
        $('.cart-item-'+item_id).css('display', 'none');
        $('#cart-total-price > b').html(data.total_cart_price);
        if (parseInt(data.total, 10) == 0){
          $('.cart-wrapper').css('display', 'none');
          $('.empty-cart-inv').css('display', 'block');
        }
      }
    });
  });

  $('.add-qty').on('click', function(e){
    e.preventDefault();
    item_id = $(this).attr('data-item-id');
    data = {
      item_id: item_id
    }
    $.ajax({
      type: "GET",
      url: url_increase_qty,
      data: data,
      success: function(data){
        $('.cart-item-' + item_id + ' > .product-count').html(data.count);
        $('.cart-item-' + item_id + ' > .product-total-price').html(data.product_total_price);
        $('#cart-total-price > b').html(data.total_cart_price);
      }
    });
  });

  $('.remove-qty').on('click', function(e){
    e.preventDefault();
    item_id = $(this).attr('data-item-id');
    data = {
      item_id: item_id
    }
    $.ajax({
      type: "GET",
      url: url_decrease_qty,
      data: data,
      success: function(data){
        $('.cart-item-' + item_id + ' > .product-count').html(data.count);
        $('.cart-item-' + item_id + ' > .product-total-price').html(data.product_total_price);
        $('#cart-total-price > b').html(data.total_cart_price);
      }
    });
  });

});