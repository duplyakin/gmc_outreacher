<template>
  <div>
    <card>
      <card>
        <h4 class="card_title">F.A.Q.</h4>
        <div class="card_style">
          <template slot="header"></template>
          <el-collapse>
            <el-collapse-item title="How to add campaign?" name="1">
              <div>Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. 3 wolf moon officia aute, non cupidatat skateboard dolor brunch. Food truck quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon tempor, sunt aliqua put a bird on it squid single-origin coffee nulla assumenda shoreditch et. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident. Ad vegan excepteur butcher vice lomo. Leggings occaecat craft beer farm-to-table, raw denim aesthetic synth nesciunt you probably haven't heard of them accusamus labore sustainable VHS.</div>
            </el-collapse-item>
            <el-collapse-item title="How to do smth?" name="2">
              <div>Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. 3 wolf moon officia aute, non cupidatat skateboard dolor brunch. Food truck quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon tempor, sunt aliqua put a bird on it squid single-origin coffee nulla assumenda shoreditch et. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident. Ad vegan excepteur butcher vice lomo. Leggings occaecat craft beer farm-to-table, raw denim aesthetic synth nesciunt you probably haven't heard of them accusamus labore sustainable VHS.</div>
            </el-collapse-item>
            <el-collapse-item title="How to token?" name="3">
              <div>Anim pariatur cliche reprehenderit, enim eiusmod high life accusamus terry richardson ad squid. 3 wolf moon officia aute, non cupidatat skateboard dolor brunch. Food truck quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon tempor, sunt aliqua put a bird on it squid single-origin coffee nulla assumenda shoreditch et. Nihil anim keffiyeh helvetica, craft beer labore wes anderson cred nesciunt sapiente ea proident. Ad vegan excepteur butcher vice lomo. Leggings occaecat craft beer farm-to-table, raw denim aesthetic synth nesciunt you probably haven't heard of them accusamus labore sustainable VHS.</div>
            </el-collapse-item>
          </el-collapse>
        </div>
      </card>
      <card>
        <h4 class="card_title">Contact information</h4>
        <p class="contacts">E-mail</p>
        <p>outreacher24@gmail.com</p>
        <p class="contacts">LinkedIn</p>
        <p>linkedin.com/outreacher24</p>
        <p class="contacts">Facebook</p>
        <p>facebook.com/outreacher24</p>
      </card>
    </card>
  </div>
</template>
<script>
import { Collapse, CollapseItem } from "element-ui";
import VueTabs from "vue-nav-tabs";

export default {
  components: {
    [Collapse.name]: Collapse,
    [CollapseItem.name]: CollapseItem
  },
  data() {
    return {
      activeNames: ["1"]
    };
  },
  methods: {
    handleChange(val) {
      console.log(val);
    }
  }
};
</script>
<style>
.card_title {
  text-align: center;
  font-size: 35px;
  font-weight: 500;
}
.card_style {
  text-align: center;
}
.contacts {
  font-size: 20px;
  font-weight: 600;
  height: 10px;
}
</style>
