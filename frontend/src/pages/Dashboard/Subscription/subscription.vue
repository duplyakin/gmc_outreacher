<template>
    <div>      
      <card>
        <div class="row">
            <div class="col-4 d-flex align-self-center">
                <h3>
                <i class="nc-icon nc-single-copy-04"></i> Subscription settings
                </h3>
            </div>
            <div class="col-8 d-flex flex-row-reverse align-self-center">
            </div>
        </div>
        </card>
        
        <card>
                <div class="col-12">
                  <el-table
                  stripe
                  style="width: 100%;"
                  :data="tableData"
                  max-height="500"
                  border>
                  <el-table-column
                    prop="plan"
                    label="Subscription plan"
                    width="180">
                  </el-table-column>
                  <el-table-column
                    prop="price"
                    label="Price"
                    width="180">
                  </el-table-column>
                 
                  <el-table-column
                    prop="link"
                    label=""
                    width="180">
                    <template slot-scope="scope">
                      <a @click.prevent="activateSubscription(scope.row)" href="#">Activate</a>
                  </template>
                  </el-table-column>
                </el-table>
                </div>
        </card>   


    </div>
  
  </template>
  <script>
  import axios from "@/api/axios-auth";
  import { Table, TableColumn } from "element-ui";
    

  export default {
    components: {
      [Table.name]: Table,
      [TableColumn.name]: TableColumn
    },
    data() {
      return {
        tableData: [{
          plan: 'Solopreneur',
          price: '$19/month',
          link: 'solo',
        }, {
          plan: 'Agency',
          price: '$49/month',
          link: 'agency',
        }]
      
      };
    },
    methods: {
        activateSubscription(data){
          var plan = data.link;

          if (plan == 'solo'){
            Paddle.Checkout.open({ product: 599188 });
          }else{
            Paddle.Checkout.open({ product: 599189 });
          }
        }
    },
    async mounted() {
      Paddle.Setup({ vendor: 117323 });
    },
    created() {
    }
  };
  </script>
  <style>
  .card_title {
    text-align: center;
    font-size: 35px;
    font-weight: 500;
  }
  .info {
    font-size: 20px;
    font-weight: 600;
    height: 10px;
  }
  </style>
  