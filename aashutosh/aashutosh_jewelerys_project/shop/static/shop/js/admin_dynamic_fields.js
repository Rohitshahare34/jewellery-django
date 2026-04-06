document.addEventListener('DOMContentLoaded', function() {
    const metalType = document.getElementById('id_metal_type');

    function toggleFields() {
        const isGold = metalType.value === 'Gold';
        const goldFields = ['id_gold_purity', 'id_gold_weight', 'id_gold_value'];
        const silverFields = ['id_silver_purity', 'id_silver_weight', 'id_silver_value'];

        goldFields.forEach(id => {
            const field = document.getElementById(id).closest('.form-row');
            field.style.display = isGold ? '' : 'none';
        });
        silverFields.forEach(id => {
            const field = document.getElementById(id).closest('.form-row');
            field.style.display = isGold ? 'none' : '';
        });
    }

    if (metalType) {
        toggleFields();
        metalType.addEventListener('change', toggleFields);
    }
});
