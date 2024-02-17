

   // make an AJAX request to your Django view that returns the count of items in the cart
   fetch('/mycandidates_count')
   .then(response => response.json())
   .then(data => {
     // update the count in the HTML
     document.getElementById('mycandidates_count').textContent = data.count;
   })
   .catch(error => {
     console.error('Error fetching candidate count:', error);
   });





   fetch('/inprogress_candidates')
   .then(response => response.json())
   .then(data => {
     // update the count in the HTML
     document.getElementById('inprogressCandidatesCount').textContent = data.count;
   })
   .catch(error => {
     console.error('Error fetching candidate count:', error);
   });


   
   fetch('/rejected_candidates')
   .then(response => response.json())
   .then(data => {
     // update the count in the HTML
     document.getElementById('rejectedCandidatesCount').textContent = data.count;
   })
   .catch(error => {
     console.error('Error fetching candidate count:', error);
   });

   
   fetch('/selected_candidates')
   .then(response => response.json())
   .then(data => {
     // update the count in the HTML
     document.getElementById('selectedCandidatesCount').textContent = data.count;
   })
   .catch(error => {
     console.error('Error fetching candidate count:', error);
   });
   

   