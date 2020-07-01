<template>
    <div>
      <card>
        <div class="col-4 d-flex align-self-center">
          <h3>
            <i class="nc-icon nc-circle-09"></i> Subscription settings
          </h3>
        </div>
        <card>
            <div id="paddle">
                <a @click.prevent="agencyPlanActivate()" href="#">Activate Agency plan</a>
                <a @click.prevent="solopreneurPlanActivate()" href="#">Activate Solopreneur plan</a>

            </div>
        </card>
      </card>
  
      <modals-container/>
    </div>
  
  </template>
  <script>
  import axios from "@/api/axios-auth";
  import { Notification, Select, Option } from "element-ui";
    

  export default {
    data() {
      return {
        user_data: {}
      };
    },
    methods: {
        agencyPlanActivate(){
            Paddle.Checkout.open({ product: 599189 });
        },
        solopreneurPlanActivate(){
          Paddle.Checkout.open({ product: 599188 });
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
  