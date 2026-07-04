def linear_search(data, keyword, field='name'):
    hasil = []
    keyword_lower = keyword.lower().strip()

    for item in data:
        nilai_field = str(getattr(item, field, '')).lower()
        if keyword_lower in nilai_field:
            hasil.append(item)

    return hasil

def binary_search_by_nama(data_sorted, keyword):
    hasil = []
    keyword_lower = keyword.lower().strip()

    data_list = list(data_sorted)
    data_list.sort(key=lambda x: x.name.lower())

    n = len(data_list)
    if n == 0 or not keyword_lower:
        return hasil

    left, right = 0, n - 1
    first_match_idx = -1

    while left <= right:
        mid = (left + right) // 2
        mid_name = data_list[mid].name.lower()

        if mid_name.startswith(keyword_lower):
            first_match_idx = mid
            right = mid - 1
        elif mid_name < keyword_lower:
            left = mid + 1
        else:
            right = mid - 1

    if first_match_idx != -1:
        i = first_match_idx
        while i < n and data_list[i].name.lower().startswith(keyword_lower):
            hasil.append(data_list[i])
            i += 1

    return hasil

# Sorting Algorithms
def bubble_sort(data, field='name', ascending=True):
    data_list = list(data)
    n = len(data_list)

    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            val_j = getattr(data_list[j], field)
            val_next = getattr(data_list[j + 1], field)

            if isinstance(val_j, str):
                val_j = val_j.lower()
                val_next = val_next.lower()

            should_swap = val_j > val_next if ascending else val_j < val_next

            if should_swap:
                data_list[j], data_list[j + 1] = data_list[j + 1], data_list[j]
                swapped = True

        if not swapped:
            break

    return data_list

def selection_sort(data, field='price', ascending=True):
    data_list = list(data)
    n = len(data_list)

    for i in range(n):
        extremum_idx = i

        for j in range(i + 1, n):
            val_j = getattr(data_list[j], field)
            val_ext = getattr(data_list[extremum_idx], field)

            if isinstance(val_j, str):
                val_j = val_j.lower()
                val_ext = val_ext.lower()

            if ascending and val_j < val_ext:
                extremum_idx = j
            elif not ascending and val_j > val_ext:
                extremum_idx = j

        if extremum_idx != i:
            data_list[i], data_list[extremum_idx] = data_list[extremum_idx], data_list[i]

    return data_list

def insertion_sort(data, field='stock', ascending=True):
    data_list = list(data)
    n = len(data_list)

    for i in range(1, n):
        key_item = data_list[i]
        key_val = getattr(key_item, field)

        if isinstance(key_val, str):
            key_val = key_val.lower()

        j = i - 1

        while j >= 0:
            compare_val = getattr(data_list[j], field)
            if isinstance(compare_val, str):
                compare_val = compare_val.lower()

            condition = compare_val > key_val if ascending else compare_val < key_val

            if condition:
                data_list[j + 1] = data_list[j]
                j -= 1
            else:
                break

        data_list[j + 1] = key_item

    return data_list

def get_algorithm_info(algo_name):
    info = {
        'linear_search': {
            'nama': 'Linear Search',
            'deskripsi': 'Memeriksa setiap elemen satu per satu dari awal hingga akhir.',
            'kompleksitas': 'O(n)',
            'keunggulan': 'Sederhana, bekerja pada data tidak terurut.',
            'kelemahan': 'Lambat untuk data besar.',
        },
        'binary_search': {
            'nama': 'Binary Search',
            'deskripsi': 'Membagi data menjadi dua bagian, mencari di bagian yang relevan.',
            'kompleksitas': 'O(log n)',
            'keunggulan': 'Sangat cepat untuk data besar.',
            'kelemahan': 'Data harus sudah terurut terlebih dahulu.',
        },
        'bubble_sort': {
            'nama': 'Bubble Sort',
            'deskripsi': 'Membandingkan dan menukar elemen berdekatan berulang kali.',
            'kompleksitas': 'O(n²)',
            'keunggulan': 'Mudah dipahami, deteksi data terurut.',
            'kelemahan': 'Lambat untuk data besar.',
        },
        'selection_sort': {
            'nama': 'Selection Sort',
            'deskripsi': 'Memilih elemen minimum/maksimum dan menempatkannya ke posisi yang benar.',
            'kompleksitas': 'O(n²)',
            'keunggulan': 'Jumlah swap minimal.',
            'kelemahan': 'Tidak efisien untuk data besar.',
        },
        'insertion_sort': {
            'nama': 'Insertion Sort',
            'deskripsi': 'Menyisipkan setiap elemen ke posisi yang tepat, seperti menyusun kartu.',
            'kompleksitas': 'O(n²) worst, O(n) best',
            'keunggulan': 'Efisien untuk data kecil atau hampir terurut.',
            'kelemahan': 'Tidak efisien untuk data besar yang acak.',
        },
    }
    return info.get(algo_name, {})
