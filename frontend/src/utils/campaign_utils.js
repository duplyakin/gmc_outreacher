import axios from "@/api/axios-auth";


  async function load_previous_step(path, campaign_data) {
    let data = new FormData()
    let previous_step = {}

    data.append("action", "back")
    data.append("_data", campaign_data)

    return axios
      .post(path, data)
      .then(res => {
        let r = res.data
        if (r.hasOwnProperty('error') && r.error !== 0) {
          previous_step.error = "Error loading data " + r.msg + " Error:" + r.error
        } else {
          if (r.hasOwnProperty('previous_step') && r.previous_step) {
            previous_step.path = r.previous_step
          } else {
            previous_step.error = 'Server error: no previous step'
          }
        }

        return previous_step
      })
      .catch(error => {
        previous_step.error = "Error loading data. ERROR: " + error
        return previous_step
      })
  }

  async function load_next_step(path, campaign_data) {
    let data = new FormData()
    let next_step = {}

    data.append("action", "next")
    data.append("_data", campaign_data)

    return axios
      .post(path, data)
      .then(res => {
        let r = res.data
        if (r.hasOwnProperty('error') && r.error !== 0) {
          next_step.error = "Error loading data " + r.msg + " Error:" + r.error
        } else {
          if (r.hasOwnProperty('next_step')) {
            next_step.path = r.next_step
          } else {
            // it was last step
            next_step.path = '/campaigns'
          }
        }

        return next_step
      })
      .catch(error => {
        next_step.error = "Error loading data. ERROR: " + error
        return next_step
      })
  }

  async function load_data(path, campaign_data, list_data) {
    let result = {}

    return axios
      .get(path)
      .then(res => {
        let r = res.data
        if (r.hasOwnProperty('error') && r.error !== 0) {
          result.error = "Error loading data " + r.msg + " Error:" + r.error
        } else {
          if (r.hasOwnProperty('action')) {
            result.action = r.action
          } else {
            result.error = "Server error: no action"
          }

          if (r.hasOwnProperty('data')) {
            result.campaign_data = deserialize_campaign(campaign_data, r.data)
          }

          if (r.hasOwnProperty('list_data')) {
            result.list_data = deserialize_list_data(list_data, r.list_data)
          } else {
            result.error = "Server error: no list_data"
          }
        }

        return result
      })
      .catch(error => {
        result.error = "Error loading data. ERROR: " + error
        return result
      })
  }

  function deserialize_campaign(campaign_data, data) {
    let campaign_dict = JSON.parse(data)

    for (let key in campaign_dict) {
      if (campaign_data.hasOwnProperty(key) && campaign_dict[key]) {
        /* Check or validate for custom keys here */
        if (key == "templates") {
          let email_templates = campaign_dict[key].email || null
          if (email_templates) {
            campaign_data[key].email = email_templates
          }

          let linkedin_templates = campaign_dict[key].linkedin || null
          if (linkedin_templates) {
            campaign_data[key].email = linkedin_templates
          }
        } else {
          campaign_data[key] = campaign_dict[key]
        }
      }
    }

    return campaign_data
  }

  function deserialize_list_data(list_data, from_data) {
    //console.log(from_data)
    for (let key in from_data) {
      if (list_data.hasOwnProperty(key) && from_data[key]) {
        list_data[key] = JSON.parse(from_data[key])
      }
    }

    return list_data
  }

export default {
    load_previous_step,
    load_next_step,
    load_data,
  }