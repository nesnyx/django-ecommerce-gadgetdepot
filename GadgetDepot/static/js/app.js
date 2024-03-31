window.paypal
  .Buttons({

    style: {
      color:  'blue',
      shape:  'rect',
      label:  'pay',
      height: 40
  },

  createOrder: function(data,actions){
    return actions.order.create({
      purchase_units : [{
        amount : {
          value : '88.48'
        }
      }]
    })
  },

  onApprove: function(data, actions){
    return actions.order.capture().then(function(details){
      alert('Transaction completed by ' + details.payer.name.given_name + '!')
    });
  }
  }
    ).render("#paypal-button-container");
  
// Example function to show a result to the user. Your site's UI library can be used instead.
function resultMessage(message) {
  const container = document.querySelector("#result-message");
  container.innerHTML = message;
}
