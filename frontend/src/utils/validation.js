import { forOwn, isFunction } from "lodash";

export const validationErrorMessages = {
  between: ({ min, max }) => `Sólo valores entre ${min} y ${max}`,
  maxLength: ({ max }) => `Longitud máxima ${max}`,
  maxValue: ({ max }) => `Valor máximo ${max}`,
  minLength: ({ min }) => `Longitud mínima ${min}`,
  minValue: ({ min }) => `Valor mínimo ${min}`,
  numeric: "Valor numérico",
  required: "Campo requerido",
};

export function buildValidationErrorMessages(field) {
  const errors = [];
  if (!field.$dirty) {
    return errors;
  }
  forOwn(field, (value, key, item) => {
    if (!key.startsWith("$") && !value) {
      const msg = this.validationErrorMessages[key];
      const actualMsg = isFunction(msg) ? msg(item.$params[key]) : msg;
      errors.push(actualMsg || "[Mensaje de error no disponible]");
    }
  });
  return errors;
}
