var updateBtns = document.getElementsByClassName('update-order')

console.log('inside order.js file')
console.log('Var updateBtns' + updateBtns)
console.log('Var updateBtns length: ' + updateBtns.length)
//console.log('productId:', productId, 'Action:', action)
//console.log('USER:', user)
//console.log('CUSTOMER:', customer)


for (i = 0; i < updateBtns.length; i++) {
	console.log('Inside for loop ' + i)
	console.log('updateBtns:' + updateBtns[i])
	
	//console.log('USER:', user)
	//console.log('CUSTOMER:', customer)
	//console.log('productId:', productId, 'Action:', action)

	updateBtns[i].addEventListener('click', function () {
		console.log('this.dataset:' + this.dataset)
		console.log(this.dataset)
		console.log('(this.dataset.dish: ' + this.dataset.dish)
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log(updateBtns[i])
		console.log('productId:', productId, 'Action:', action)
		//console.log('USER:', user)
		//console.log('CUSTOMER:', customer)
		console.log('Inside for loop ' + i)
		
		/*if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}*/
		updateUserOrder(productId, action)
	})
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')
	console.log('Inside updateUserOrder Function... ')
		var url = '/update_item/'
		//var csrftoken = getToken('csrftoken')
		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}

function testFunc(orderID, itemID, reqUser, action) {
	console.log('inside testFunc')
	console.log('orderID: ' + orderID)
	console.log('itemID: ' + itemID)
	console.log('action: ' + action)
	console.log('reqUser: ' + reqUser)
}