<template>
  <v-container fluid>
    <v-row>
      <v-col class="text-center">
        <h1>Error 404</h1>
        <h2>La ruta introducida no existe</h2>
      </v-col>
    </v-row>
    <v-row>
      <v-col class="text-center">
        <a href="https://elgoog.im/t-rex/v2/" target="_blank" rel="noopener noreferrer">
          <img src="@/assets/dino.png" alt="Google Chrome's dinosaur" />
        </a>
      </v-col>
    </v-row>
    <v-row>
      <v-col class="text-center">
        <v-btn outlined x-large color="primary" @click.prevent="$router.go(-1)">Volver</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
