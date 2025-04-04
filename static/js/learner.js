// Generate and store learner_id if it doesn't exist
(function() {
    if (!localStorage.getItem('learner_id')) {
        const learnerId = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0;
            return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
        });
        localStorage.setItem('learner_id', learnerId);
    }

    // Set learner_id in the hidden form field when the page loads
    const learnerId = localStorage.getItem('learner_id');
    document.getElementById('learner_id').value = learnerId;

})();
