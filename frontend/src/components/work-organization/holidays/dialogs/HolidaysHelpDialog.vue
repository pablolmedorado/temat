<template>
  <v-dialog v-model="showDialog" v-bind="$attrs" :max-width="500" @click:outside="close" @keydown.esc="close">
    <v-card>
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Código de colores </v-toolbar-title>
      </v-toolbar>
      <v-card-text class="pa-0">
        <v-simple-table>
          <template #default>
            <thead>
              <tr>
                <th scope="col" class="text-left">Color</th>
                <th scope="col" class="text-left">Significado</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><v-chip color="grey" dark>Gris</v-chip></td>
                <td>Día ya solicitado (sólo vista de usuario).</td>
              </tr>
              <tr>
                <td><v-chip color="black" dark>Negro</v-chip></td>
                <td>Existe un evento marcado como importante planificado para ese día.</td>
              </tr>
              <tr>
                <td><v-chip color="green" dark>Verde</v-chip></td>
                <td>
                  Al menos un usuario ha pedido vacaciones ese día, pero la cantidad de usuarios es inferior al 20%.
                </td>
              </tr>
              <tr>
                <td><v-chip color="orange" dark>Naranja</v-chip></td>
                <td>Entre un 20 y un 50% de los usuarios han solicitado vacaciones ese día.</td>
              </tr>
              <tr>
                <td><v-chip color="red" dark>Rojo</v-chip></td>
                <td>Más del 50% de los usuarios han solitado vacaciones ese día.</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="close"> Volver </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import DialogMixin from "@/mixins/dialog-mixin";

export default {
  name: "HolidaysHelpDialog",
  mixins: [DialogMixin],
};
</script>
