@bp_dashboard.route('/campaigns/create', methods=['POST'])
@bp_dashboard.route('/campaigns/create/<action>/<step>', methods=['POST'])
@auth_required
def campaigns_create(action=None, step=None):
    current_user = g.user

    try:
        if request.method == 'POST':
            if not action:
                
            elif action == 'publish':


            data = int(request.form.get('_data'))
            if not data:
                raise Exception("Please fill the fields")
            
            form.save_step(step=step, data=data)

            next_data = form.next_step()
            result['data'] = json.dumps(next_data)
    except Exception as e:
        #TODO: change to loggin
        print(e)
        traceback.print_exc()

        result['code'] = -1
        result['msg'] = str(e)

    return jsonify(result), 200

