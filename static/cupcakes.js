const BASE_URL = "http://127.0.0.1:5000/api";


// Have cupckaes be display in a list format

function generateCupcakeHTML(cupcake){
    return `<div data-cupcake-id=${cupcake.id}>
            <li>${cupcake.flavor}/${cupcake.size}/${cupcake.rating}
            <button id='delete-button'>x</button>
            </li>
            <img class='cupcake-image' src='${cupcake.image}'>
            
            </div>`;
    }

// Show cupcakes when page is rendered
async function showInitialCupcakes(){
    const response = await axios.get(`${BASE_URL}/cupcakes`);
    console.log(response);

    for (let cupcakeData of response.data.cupcakes){
        let newCupcake = $(generateCupcakeHTML(cupcakeData));
        $('#cupcakes-list').append(newCupcake);
    }
}


//Handle adding new cupcake form

$('#new-cupcake-form').on('submit', async function(event){
    event.preventDefault();

    let flavor = $('#form-flavor').val();
    let size = $('#form-size').val();
    let rating = $('#form-rating').val();
    let image = $('#form-image').val();
    
    const newCupakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        size,
        rating,
        image
    });

    let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
    $('#cupcakes-list').append(newCupcake);
    $('#new-cupcake-form').trigger('reset');
});

$('#cupcakes-list').on('click','#delete-button', async function (event){
    event.preventDefault()
    let $cupcake=$(event.target).closest("div");
    let cupcakeId = $cupcake.attr('data-cupcake-id');

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});

$(showInitialCupcakes);