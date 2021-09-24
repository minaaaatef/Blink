<template>
  <v-container>
  <v-card class="mt-3" v-for="item in ListData" :key="item.id">
    <v-card-title v-for="attr in attribute" :key="attr.name">

      <h5 v-if="attr.type === 'select'" >  {{attr.name}} : {{attr.data[item[attr.name]]}} </h5>
      <h5 v-if="attr.type === 'text'" >    {{attr.name}} : {{item[attr.name]}}</h5>
      <h5 v-if="attr.type === 'number'" >    {{attr.name}} : {{item[attr.name].toFixed(2)}}</h5>
      <h5 v-if="attr.type === 'percentage'" >    {{attr.name}} : {{ (item[attr.name] * 100).toFixed(2) }} %</h5>
      <h5 v-if="attr.type === 'nested' & attr.DataType === 'select' " >    {{attr.name}} : {{ attr.data[item[attr.parent][attr.name]] }}</h5>
    </v-card-title>
    <v-card-actions>
      <div  v-for="action in actions" :key="action.name">
        <v-form>
        <v-btn v-if=" action.key === 'id' && (item[action.ifTruecondition] || !item[action.ifFalsecondition])" :class="action.class" @click="action.Function(item.id)"> {{action.name}}  </v-btn>
        <v-btn v-if=" action.key === 'item' && (item[action.ifTruecondition] || !item[action.ifFalsecondition])" :class="action.class" @click="action.Function(item)"> {{action.name}}  </v-btn>
          </v-form>
      </div>

    </v-card-actions>
  </v-card>
    </v-container>

</template>

<script>
export default {
  data: () => ({
    ListData: []
  }),

  props: [
    'url',
    'attribute',
    'actions'
  ],
  beforeMount() {
    const token = window.localStorage.getItem('token')
    const requestOptions = {
      method: 'GET',
      headers: { Authorization: 'Token ' + token, 'Content-Type': 'application/json' }
    }

    fetch(this.url, requestOptions)
      .then(response => {
        response.json().then(data => {
          console.log(data)
          this.ListData = data
        })
      }).catch(function (error) {
        console.log(error)
      })
  }
}
</script>
