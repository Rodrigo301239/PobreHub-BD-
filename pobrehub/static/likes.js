document.querySelectorAll('input[type="radio"]').forEach(radio => {
    radio.addEventListener('change', function () {
      const form = this.closest('.like-form');
      const postId = form.dataset.postId;
  
      console.log("ID do post:", postId);
      console.log("Valor escolhido:", this.value);
  
      const formData = new FormData(form);
      
      formData.append('post_id', postId);
      formData.append('like', this.value);
    
      fetch('/like', {
        method: 'POST',
        body: formData
      })
      .then(response => response.text())
      .then(data => {
        console.log(data); // Resposta do servidor
      })
      .catch(error => {
        console.error('Erro:', error);
      });
    });
  });