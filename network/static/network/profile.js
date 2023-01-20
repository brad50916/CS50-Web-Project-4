document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.like').forEach(button => button.addEventListener('click', function() {
        document.querySelector('#like'+this.value).style.display = 'none';
        document.querySelector('#unlike'+this.value).style.display = 'block';
        fetch(`/like/${this.value}`, {
            method:'PUT',
            body: JSON.stringify({
                like: true
            })
        })
        var inc = parseInt(document.querySelector('#number'+this.value).innerHTML);
        inc++;
        document.querySelector('#number'+this.value).innerHTML = inc;
    }));
    document.querySelectorAll('.unlike').forEach(button => button.addEventListener('click', function() {
        document.querySelector('#unlike'+this.value).style.display = 'none';
        document.querySelector('#like'+this.value).style.display = 'block';
        fetch(`/like/${this.value}`, {
            method:'PUT',
            body: JSON.stringify({
                like: false
            })
        })
        var dec = parseInt(document.querySelector('#number'+this.value).innerHTML);
        dec--;
        document.querySelector('#number'+this.value).innerHTML = dec;
    }));
    document.querySelectorAll('.exist').forEach(e => {
        var exist = e.getAttribute('value')
        document.querySelector('#like'+exist).style.display = 'none';
        document.querySelector('#unlike'+exist).style.display = 'block';
    })
    document.querySelectorAll('.edit').forEach(button => button.addEventListener('click', function() {
        document.querySelector('#edit'+ this.value).style.display = 'none';
        document.querySelector('#content'+ this.value).style.display = 'none';
        document.querySelector('#edit_form'+ this.value).style.display = 'block'
        edit(this.value)
    }));
    
});

function edit(id) {
    document.querySelector("#edit_form"+id).onsubmit = function() {
        event.preventDefault();
        fetch(`/edit/${id}`, {
        method: 'POST',
        body: JSON.stringify({
            content: document.querySelector('#compose_body'+id).value
        })
        })
        .then(response => response.json())
        .then(result => {
        // Print result
        console.log(result);
        });
        document.querySelector('#content'+ id).style.display = 'block';
        document.querySelector('#edit'+ id).style.display = 'block';
        document.querySelector('#edit_form'+ id).style.display = 'none';
        document.querySelector('#content'+ id).innerHTML=document.querySelector('#compose_body'+id).value
    }
}