<template>
  <div>
    <div class="horizontal-divider my-2"></div>
    <table>
      <thead>
        <th class="first-row">key</th><th>value</th>
      </thead>
      <tbody>
        <tr v-for="(value, key) in sample" :key="key">
          <td>{{key}}</td>
          <td v-if="key === '_annotations'">
            <table>
              <thead><th class="first-row">key</th><th>value</th></thead>
              <tbody v-for="(annotation, key) in value" :key="key">
                <tr v-for="(value, key) in annotation" :key="key">
                  <td>{{key}}</td>
                  <td v-if="key === '_relationArguments'">
                    <table>
                      <tbody v-for="(relationArgument, key) in value" :key="key">
                        <tr v-for="(value, key) in relationArgument" :key="key">
                          <td>{{key}}</td><td>{{value}}</td>
                        </tr>
                        <tr><td></td></tr>
                      </tbody>
                    </table>
                  </td>
                  <td v-else>{{value}}</td>
                </tr>
                <tr><td></td></tr>
              </tbody>
            </table>
          </td>
          <td v-else>{{value}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'ShowcaseSampleProperties',

  props: {
    sample: Object
  }
}
</script>

<style scoped lang="scss">
  table {
    width: 100%;
  }

  table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
  }

  td {
    // padding-left: 2px;
  }

  .first-row {
    width: 15%;
  }

  .horizontal-divider {
     border-top: 1.5px solid rgba(0,0,0,0.25);
     margin-left: -15px;
  }
</style>
