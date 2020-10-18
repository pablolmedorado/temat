import { forOwn, isFunction } from "lodash";

export const validationErrorMessages = {
  between: ({ min, max }) => `Sólo valores entre ${min} y ${max}`,
  maxLength: ({ maxLength }) => `Longitud máxima ${maxLength.max}`,
  maxValue: ({ max }) => `Valor máximo ${max}`,
  minLength: ({ minLength }) => `Longitud mínima ${minLength.min}`,
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
    if (!key.startsWith("$")) {
      const msg = this.validationErrorMessages[key];
      if (!value) {
        const actualMsg = isFunction(msg) ? msg(item.$params) : msg;
        errors.push(actualMsg || "[Mensaje de error no disponible]");
      }
    }
  });
  return errors;
}
