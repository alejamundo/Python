const requierePagoCheckbox = document.getElementById("requiere_pago");
const montoField = document.querySelector(".monto-field");

const requiereDepositoCheckbox = document.getElementById("requiere_deposito");
const montoDepositoField = document.querySelector(".monto-deposito-field");

// Oculta los campos inicialmente
montoField.style.display = "none";
montoDepositoField.style.display = "none";

requierePagoCheckbox.addEventListener("change", function () {
    montoField.style.display = this.checked ? "block" : "none";
});

requiereDepositoCheckbox.addEventListener("change", function () {
    montoDepositoField.style.display = this.checked ? "block" : "none";
});