import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

from product.forms import UserLoginForm
from product.models import Product, Units, Team, TeamMember, Notifications, Suppliers, ProductEntryInfo


def products(request):
    if 'name' not in request.session:
        return redirect(index)
    else:
        if request.method == 'POST':
            product_name = request.POST['product_name']
            supplier_name = request.POST['supplier_name']
            dnr = request.POST['dnr']
            quantity_value = request.POST['quantity_value']
            cone_quantity_value = request.POST['cone_quantity_value']
            unit_name = request.POST['unit_name']
            per_unit_price = request.POST['per_unit_price']
            total_unit_price = float(quantity_value) * float(per_unit_price)
            team_name = request.POST['team_name']
            cheque_no = request.POST['cheque_no']
            product = Product(product_name=product_name, product_code=dnr, unit_name=unit_name,
                              per_unit_price=per_unit_price,
                              total_unit_price=total_unit_price, team_name=team_name, quantity_value=quantity_value,
                              cone_quantity_value=cone_quantity_value)
            product.save()
            latest_id = Product.objects.latest('id')
            entry_product_info = ProductEntryInfo(productID=latest_id, chequeNo=cheque_no, supplier_name=supplier_name,
                                                  due_amount=total_unit_price)
            entry_product_info.save()
            Suppliers.objects.filter(supplier_name=supplier_name).update(due_amount=total_unit_price)
            messages.success(request, "Show Alert!!")
            return redirect(products)
        else:
            units = Units.objects.all()
            teams = Team.objects.filter(~Q(id=5), ~Q(id=6))
            team_one_suppliers = Suppliers.objects.filter(team=1)
            team_two_suppliers = Suppliers.objects.filter(team=2)
            team_three_suppliers = Suppliers.objects.filter(team=3)
            team_four_suppliers = Suppliers.objects.filter(team=4)
            team_five_suppliers = Suppliers.objects.filter(team=6)
            notifications = Notifications.objects.filter(used=0).order_by('-created_at')
            context = {
                'units': units,
                'teams': teams,
                'team_one_suppliers': team_one_suppliers,
                'team_two_suppliers': team_two_suppliers,
                'team_three_suppliers': team_three_suppliers,
                'team_four_suppliers': team_four_suppliers,
                'team_five_suppliers': team_five_suppliers,
                'page': 'add_product',
                'notifications': notifications,
            }
            storage = messages.get_messages(request)
            storage.used = True
            return render(request, 'nav.html', context)


def edit_products_success(request):
    if 'name' not in request.session:
        return redirect(index)
    else:
        if request.method == 'POST':
            id = request.POST['product_id']
            product_name = request.POST['product_name']
            dnr = request.POST['dnr']
            product = Product.objects.get(id=id)
            unit_name = request.POST['unit_name']
            per_unit_price = request.POST['per_unit_price']
            total_unit_price = product.quantity_value * float(per_unit_price)
            team_name = request.POST['team_name']
            Product.objects.filter(id=id).update(product_name=product_name, product_code=dnr, unit_name=unit_name,
                                                 per_unit_price=per_unit_price,
                                                 total_unit_price=total_unit_price, team_name=team_name,
                                                 )
            messages.success(request, "Show Alert!!")
            return redirect(product_list)
        else:
            storage = messages.get_messages(request)
            storage.used = True
            return redirect(product_list)


def purchase_products_success(request):
    if 'name' not in request.session:
        return redirect(index)
    else:
        if request.method == 'POST':
            id = request.POST['product_id']
            product = Product.objects.get(id=id)
            quantity_value = float(request.POST['quantity_value'])
            new_quantity_value = product.quantity_value + quantity_value
            cone_quantity_value = int(request.POST['cone_quantity_value'])
            new_cone_quantity_value = product.cone_quantity_value + cone_quantity_value
            supplier_name = request.POST['supplier_name']
            cheque_no = request.POST['cheque_no']
            total_unit_price = new_quantity_value * float(product.per_unit_price)
            Product.objects.filter(id=id).update(total_unit_price=total_unit_price,
                                                 quantity_value=new_quantity_value,
                                                 cone_quantity_value=new_cone_quantity_value)
            entry_product_info = ProductEntryInfo(productID=product, chequeNo=cheque_no, supplier_name=supplier_name,
                                                  due_amount=total_unit_price)
            entry_product_info.save()
            supplier = Suppliers.objects.get(supplier_name=supplier_name)
            due_amount = float(supplier.due_amount)
            new_amount = due_amount + total_unit_price
            Suppliers.objects.filter(supplier_name=supplier_name).update(due_amount=new_amount)
            messages.success(request, "Show Alert!!")
            return redirect(product_list)
        else:
            storage = messages.get_messages(request)
            storage.used = True
            return redirect(product_list)


def update_product(request):
    if 'name' not in request.session:
        return redirect(index)
    else:
        if request.method == 'POST':
            id = request.POST['product_id']
            product = Product.objects.get(id=id)
            quantity_value = float(request.POST['quantity_value'])
            rem_quantity_value = product.quantity_value - quantity_value
            used_quantity_value = product.quantity_used_value + quantity_value
            try:
                cone_quantity_value = int(request.POST['cone_quantity_value'])
            except ValueError:
                cone_quantity_value = 0

            rem_cone_quantity_value = product.cone_quantity_value - cone_quantity_value
            used_cone_quantity_value = product.cone_quantity_used_value + cone_quantity_value
            total_unit_price = float(rem_quantity_value) * float(product.per_unit_price)

            if quantity_value > product.quantity_value:
                new_quantity_value = quantity_value - product.quantity_value
                # item added
                valueProgress = 0
            elif quantity_value == product.quantity_value:
                new_quantity_value = 0
                # no change
                valueProgress = 2
            else:
                new_quantity_value = product.quantity_value - quantity_value
                # item removed
                valueProgress = 1

            notification = Notifications(changerID=TeamMember.objects.get(id=request.session['id']),
                                         changedID=Product.objects.get(id=id),
                                         changeValue=new_quantity_value,
                                         valueProgress=valueProgress)
            notification.save()

            Product.objects.filter(id=id).update(total_unit_price=total_unit_price,
                                                 quantity_used_value=used_quantity_value,
                                                 quantity_value=rem_quantity_value,
                                                 cone_quantity_value=rem_cone_quantity_value,
                                                 cone_quantity_used_value=used_cone_quantity_value)

            messages.success(request, "Show Alert!!")
            return redirect(product_list)
        else:
            storage = messages.get_messages(request)
            storage.used = True
            return render(product_list)


def edit_member_success(request):
    if 'name' not in request.session:
        return redirect(index)
    else:
        if request.method == 'POST':
            id = request.POST['member_id']
            team_member_name = request.POST['team_member_name']
            team_member_position = request.POST['team_member_position']
            team_member_username = request.POST['team_member_username']
            team_member_password = request.POST['team_member_password']
            team = request.POST['team']

            TeamMember.objects.filter(id=id).update(team_member_name=team_member_name,
                                                    team_member_position=team_member_position,
                                                    team_member_username=team_member_username,
                                                    team_member_password=team_member_password,
                                                    team=team)
            messages.success(request, "Show Alert!!")
            return HttpResponseRedirect("/member_list/%s" % team)

        else:
            storage = messages.get_messages(request)
            storage.used = True
            return redirect(team_list)


def edit_supplier_success(request):
    if 'name' not in request.session:
        return redirect(index)
    else:
        if request.method == 'POST':
            id = request.POST['supplier_id']
            supplier_name = request.POST['supplier_name']
            team = request.POST['team']

            Suppliers.objects.filter(id=id).update(supplier_name=supplier_name,
                                                   team=team)
            messages.success(request, "Show Alert!!")
            return HttpResponseRedirect("/supplier_list/%s" % team)

        else:
            storage = messages.get_messages(request)
            storage.used = True
            return redirect(supplier_team_list)


def product_list(request):
    storage = messages.get_messages(request)
    storage.used = True
    if 'name' not in request.session:
        return redirect(index)
    else:
        if request.session['team'] == 'Admin' or request.session['team'] == 'All':
            products = Product.objects.all()
            notifications = Notifications.objects.filter(used=0).order_by('-created_at')
            context = {
                'products': products,
                'notifications': notifications,
                'page': 'product_list',
            }
            return render(request, 'nav.html', context)
        else:
            products = Product.objects.filter(team_name=request.session['team'])
            context = {
                'products': products,
                'page': 'product_list',
            }
            return render(request, 'nav.html', context)


def logout_success(request):
    if 'name' not in request.session:
        return redirect(index)
    else:
        try:
            request.session.pop('name')
            return redirect(index)
        except KeyError:
            pass
            return redirect(product_list)


def team_list(request):
    if 'name' not in request.session:
        return redirect(index)
    else:
        teams = Team.objects.filter(~Q(id=5))
        one_team_count = TeamMember.objects.filter(team=1).count()
        two_team_count = TeamMember.objects.filter(team=2).count()
        three_team_count = TeamMember.objects.filter(team=3).count()
        four_team_count = TeamMember.objects.filter(team=4).count()
        six_team_count = TeamMember.objects.filter(team=6).count()
        notifications = Notifications.objects.filter(used=0).order_by('-created_at')
        context = {
            'teams': teams,
            'one_team_count': one_team_count,
            'two_team_count': two_team_count,
            'three_team_count': three_team_count,
            'four_team_count': four_team_count,
            'six_team_count': six_team_count,
            'page': 'team_list',
            'notifications': notifications,
        }
        return render(request, 'nav.html', context)


def supplier_team_list(request):
    if 'name' not in request.session:
        return redirect(index)
    else:
        teams = Team.objects.filter(~Q(id=5))
        one_team_count = Suppliers.objects.filter(team=1).count()
        two_team_count = Suppliers.objects.filter(team=2).count()
        three_team_count = Suppliers.objects.filter(team=3).count()
        four_team_count = Suppliers.objects.filter(team=4).count()
        six_team_count = Suppliers.objects.filter(team=6).count()
        notifications = Notifications.objects.filter(used=0).order_by('-created_at')
        context = {
            'teams': teams,
            'one_team_count': one_team_count,
            'two_team_count': two_team_count,
            'three_team_count': three_team_count,
            'four_team_count': four_team_count,
            'six_team_count': six_team_count,
            'page': 'supplier_team_list',
            'notifications': notifications,
        }
        return render(request, 'nav.html', context)


def history(request):
    if 'name' not in request.session:
        return redirect(index)
    else:
        Notifications.objects.all().update(used=1)
        notifications = Notifications.objects.filter(used=0).order_by('-created_at')
        all_notifications = Notifications.objects.all().order_by('-created_at')
        context = {
            'page': 'history',
            'notifications': notifications,
            'all_notifications': all_notifications,
        }
        return render(request, 'nav.html', context)


def member_list(request, id):
    if 'name' not in request.session:
        return redirect(index)
    else:
        storage = messages.get_messages(request)
        storage.used = True
        members = TeamMember.objects.filter(team=id)
        team_name = Team.objects.get(id=id)
        notifications = Notifications.objects.filter(used=0).order_by('-created_at')
        context = {
            'members': members,
            'team_name': team_name.team_name,
            'page': 'member_list',
            'notifications': notifications,

        }
        return render(request, 'nav.html', context)


def supplier_list(request, id):
    if 'name' not in request.session:
        return redirect(index)
    else:
        storage = messages.get_messages(request)
        storage.used = True
        suppliers = Suppliers.objects.filter(team=id)
        team_name = Team.objects.get(id=id)
        notifications = Notifications.objects.filter(used=0).order_by('-created_at')
        context = {
            'suppliers': suppliers,
            'team_name': team_name.team_name,
            'page': 'supplier_list',
            'notifications': notifications,

        }
        return render(request, 'nav.html', context)


def show_changes(request, id):
    if 'name' not in request.session:
        return redirect(index)
    else:
        Notifications.objects.filter(id=id).update(used=1)
        change_notifications = Notifications.objects.get(id=id)
        notifications = Notifications.objects.filter(used=0).order_by('-created_at')
        context = {
            'page': 'changes',
            'change_notifications': change_notifications,
            'notifications': notifications,

        }
        return render(request, 'nav.html', context)


def delete_product(request, id):
    if 'name' not in request.session:
        return redirect(index)
    else:
        Product.objects.get(id=id).delete()
        messages.success(request, "Show Alert!!")
        return redirect(product_list)


def delete_member(request, id):
    if 'name' not in request.session:
        return redirect(index)
    else:
        member = TeamMember.objects.get(id=id)
        team = Team.objects.get(id=member.team)
        messages.success(request, "Show Alert!!")
        member.delete()
    return HttpResponseRedirect("/member_list/%s" % team.id)


def delete_supplier(request, id):
    if 'name' not in request.session:
        return redirect(index)
    else:
        supplier = Suppliers.objects.get(id=id)
        team = Team.objects.get(id=supplier.team)
        messages.success(request, "Show Alert!!")
        supplier.delete()
    return HttpResponseRedirect("/supplier_list/%s" % team.id)


def full_pay_supplier_success(request, id):
    if 'name' not in request.session:
        return redirect(index)
    else:
        productinfo = ProductEntryInfo.objects.get(id=id)
        totalPaidAmount = productinfo.paid_amount + productinfo.due_amount
        ProductEntryInfo.objects.filter(id=id).update(due_amount=0,
                                                      paid_amount=totalPaidAmount)
        supplier = Suppliers.objects.get(supplier_name=productinfo.supplier_name)
        supplier_new_due_amount = supplier.due_amount - productinfo.due_amount
        supplier_new_paid_amount = supplier.paid_amount + productinfo.due_amount
        Suppliers.objects.filter(id=supplier.id).update(due_amount=supplier_new_due_amount,
                                                        paid_amount=supplier_new_paid_amount)
        messages.success(request, "Show Alert!!")
        context = {
            'cheque_no': productinfo.chequeNo,
            'cur_date': datetime.datetime.today(),
            'amount_due': 0,
            'product': productinfo.productID.product_name + " " + productinfo.productID.product_code,
            'rate': productinfo.productID.per_unit_price,
            'quantity': (float(productinfo.paid_amount) + float(productinfo.due_amount)) / float(
                productinfo.productID.per_unit_price),
            'unit': productinfo.productID.unit_name,
            'total_price': (float(productinfo.paid_amount) + float(productinfo.due_amount)),
            'amount_paid': (float(productinfo.paid_amount) + float(productinfo.due_amount)),
            'balance_due': 0,
        }

        return render(request, 'partials/pdf.html', context)


def supplier_payment(request):
    if 'name' not in request.session:
        return redirect(index)
    else:
        if request.method == 'POST':
            id = request.POST['info_id']
            entryInfo = ProductEntryInfo.objects.get(id=id)
            supplier = Suppliers.objects.get(supplier_name=entryInfo.supplier_name)
            payment_value = float(request.POST['payment_value'])
            new_entryInfo_dueAmount = float(entryInfo.due_amount) - payment_value
            new_entryInfo_paid_amount = float(entryInfo.paid_amount) + payment_value
            new_supplier_due_amount = float(supplier.due_amount) - payment_value
            new_supplier_paid_amount = float(supplier.paid_amount) + payment_value
            ProductEntryInfo.objects.filter(id=id).update(due_amount=new_entryInfo_dueAmount,
                                                          paid_amount=new_entryInfo_paid_amount)
            Suppliers.objects.filter(supplier_name=entryInfo.supplier_name).update(due_amount=new_supplier_due_amount,
                                                                                   paid_amount=new_supplier_paid_amount)
            messages.success(request, "Show Alert!!")
            context = {
                'cheque_no': entryInfo.chequeNo,
                'supplier_name': entryInfo.supplier_name,
                'cur_date': datetime.datetime.today(),
                'amount_due': new_entryInfo_dueAmount,
                'product': entryInfo.productID.product_name + " " + entryInfo.productID.product_code,
                'rate': entryInfo.productID.per_unit_price,
                'quantity': (float(entryInfo.paid_amount) + float(entryInfo.due_amount)) / float(
                    entryInfo.productID.per_unit_price),
                'unit': entryInfo.productID.unit_name,
                'total_price': (entryInfo.paid_amount + entryInfo.due_amount),
                'amount_paid': new_entryInfo_paid_amount,
                'balance_due': new_entryInfo_dueAmount,
            }
            return render(request, 'partials/pdf.html', context)
        else:
            storage = messages.get_messages(request)
            storage.used = True
            return render(supplier_team_list)


def edit_product(request, id):
    if 'name' not in request.session:
        return redirect(index)
    else:
        product = Product.objects.get(id=id)
        units = Units.objects.all()
        teams = Team.objects.filter(~Q(id=5), ~Q(id=6))
        notifications = Notifications.objects.filter(used=0).order_by('-created_at')
        context = {
            'product': product,
            'units': units,
            'teams': teams,
            'page': 'edit_product',
            'notifications': notifications
        }
    return render(request, 'nav.html', context)


def purchase_product(request, id):
    if 'name' not in request.session:
        return redirect(index)
    else:
        product = Product.objects.get(id=id)
        team = Team.objects.get(team_name=product.team_name)
        suppliers = Suppliers.objects.filter(team=team.id)
        notifications = Notifications.objects.filter(used=0).order_by('-created_at')
        context = {
            'product': product,
            'suppliers': suppliers,
            'page': 'purchase_product',
            'notifications': notifications
        }
    return render(request, 'nav.html', context)


def edit_member(request, id):
    if 'name' not in request.session:
        return redirect(index)
    else:
        member = TeamMember.objects.get(id=id)
        teams = Team.objects.filter(~Q(id=5))
        notifications = Notifications.objects.filter(used=0).order_by('-created_at')
        context = {
            'member': member,
            'teams': teams,
            'page': 'edit_member',
            'notifications': notifications
        }
    return render(request, 'nav.html', context)


def edit_supplier(request, id):
    if 'name' not in request.session:
        return redirect(index)
    else:
        supplier = Suppliers.objects.get(id=id)
        teams = Team.objects.filter(~Q(id=5))
        notifications = Notifications.objects.filter(used=0).order_by('-created_at')
        context = {
            'supplier': supplier,
            'teams': teams,
            'page': 'edit_supplier',
            'notifications': notifications
        }
    return render(request, 'nav.html', context)


def pay_supplier(request, id):
    if 'name' not in request.session:
        return redirect(index)
    else:
        supplier = Suppliers.objects.get(id=id)
        producEntryInfo = ProductEntryInfo.objects.filter(supplier_name=supplier.supplier_name)
        notifications = Notifications.objects.filter(used=0).order_by('-created_at')
        context = {
            'productEntryInfos': producEntryInfo,
            'supplier': supplier,
            'page': 'pay_supplier',
            'notifications': notifications
        }
    return render(request, 'nav.html', context)


def add_member(request):
    if 'name' not in request.session:
        return redirect(index)
    else:
        if (request.method == 'POST'):
            team_member_name = request.POST['team_member_name']
            team_member_position = request.POST['team_member_position']
            team_member_username = request.POST['team_member_username']
            team_member_password = request.POST['team_member_password']
            team = request.POST['team']

            member = TeamMember(team_member_name=team_member_name, team_member_position=team_member_position,
                                team_member_username=team_member_username, team_member_password=team_member_password,
                                team=team)
            member.save()
            messages.success(request, "Show Alert!!")
            return redirect(add_member)
        else:
            teams = Team.objects.filter(~Q(id=5))
            notifications = Notifications.objects.filter(used=0).order_by('-created_at')
            context = {
                'teams': teams,
                'page': 'add_member',
                'notifications': notifications
            }
            storage = messages.get_messages(request)
            storage.used = True
            return render(request, 'nav.html', context)


def add_supplier(request):
    if 'name' not in request.session:
        return redirect(index)
    else:
        if (request.method == 'POST'):
            supplier_name = request.POST['supplier_name']
            team = request.POST['team']

            supplier = Suppliers(supplier_name=supplier_name, team=team)
            supplier.save()
            messages.success(request, "Show Alert!!")
            return redirect(add_supplier)
        else:
            teams = Team.objects.filter(~Q(id=5))
            notifications = Notifications.objects.filter(used=0).order_by('-created_at')
            context = {
                'teams': teams,
                'page': 'add_supplier',
                'notifications': notifications
            }
            storage = messages.get_messages(request)
            storage.used = True
            return render(request, 'nav.html', context)


def index(request):
    if request.method == 'POST':
        team_member_username = request.POST['team_member_username']
        team_member_password = request.POST['team_member_password']

        try:
            members = TeamMember.objects.get(team_member_username=team_member_username,
                                             team_member_password=team_member_password)
            team = Team.objects.get(id=members.team)
            if members:
                storage = messages.get_messages(request)
                storage.used = True
                request.session['name'] = members.team_member_name
                request.session['id'] = members.id
                request.session['team'] = team.team_name
                return redirect(product_list)
            else:
                messages.success(request, "Show Alert!!")
                return redirect(index)
        except ObjectDoesNotExist:
            messages.success(request, "Show Alert!!")
            return redirect(index)
    else:
        storage = messages.get_messages(request)
        storage.used = True
        try:
            if request.session['name']:
                return redirect(product_list)
            else:
                return render(request, 'index.html')
        except KeyError:
            pass
            return render(request, 'index.html')


def pdf(request, context):
    return render(request, 'partials/pdf.html', context)


def w_index(request):
    return render(request, 'Website/index.html')


def w_about(request):
    return render(request, 'Website/about.html')


def w_projects(request):
    return render(request, 'Website/projects.html')


def w_contact(request):
    return render(request, 'Website/contact.html')


def w_machineries(request):
    return render(request, 'Website/machineries.html')


def w_products(request):
    return render(request, 'Website/products.html')
