import honeycomb_io
import pandas as pd
import tqdm
import tqdm.notebook
import datetime
import dateutil
import random
import uuid
import logging

logger = logging.getLogger(__name__)

def generate_interaction_data(
    start_date,
    end_date,
    time_zone_name,
    weekdays_only='True',
    environment_id=None,
    environment_name=None,
    start_hour = 8,
    end_hour = 16,
    idle_duration_minutes=20,
    tray_carry_duration_seconds=10,
    material_usage_duration_minutes=40,
    step_size_seconds=0.1,
    interaction_source_type='INFERRED',
    output_format='list',
    write_to_honeycomb=False,
    chunk_size=1000,
    client=None,
    uri=None,
    token_uri=None,
    audience=None,
    client_id=None,
    client_secret=None,
    progress_bar=False,
    notebook=False,
):
    if weekdays_only:
        freq='B'
    else:
        freq='D'
    date_range = pd.date_range(
        start=start_date,
        end=end_date,
        freq=freq
    )
    date_list = [datetime.date() for datetime in date_range]
    tray_interactions = list()
    material_interactions = list()
    if progress_bar:
        if notebook:
            date_iterator = tqdm.notebook.tqdm(date_list)
        else:
            date_iterator = tqdm.tqdm(date_list)
    else:
        date_iterator = date_list
    for target_date in date_iterator:
        tray_interactions_day, material_interactions_day = generate_interaction_data_day(
            target_date=target_date,
            time_zone_name=time_zone_name,
            environment_id=environment_id,
            environment_name=environment_name,
            start_hour = start_hour,
            end_hour = end_hour,
            idle_duration_minutes=idle_duration_minutes,
            tray_carry_duration_seconds=tray_carry_duration_seconds,
            material_usage_duration_minutes=material_usage_duration_minutes,
            step_size_seconds=0.1,
            interaction_source_type=interaction_source_type,
            output_format='list',
            write_to_honeycomb=write_to_honeycomb,
            chunk_size=chunk_size,
            client=client,
            uri=uri,
            token_uri=token_uri,
            audience=audience,
            client_id=client_id,
            client_secret=client_secret,
            progress_bar=progress_bar,
            notebook=notebook
        )
        tray_interactions.extend(tray_interactions_day)
        material_interactions.extend(material_interactions_day)
    if output_format == 'list':
        return tray_interactions, material_interactions
    elif output_format == 'dataframe':
        tray_interactions_df = pd.DataFrame(tray_interactions)
        tray_interactions_df['start'] = pd.to_datetime(tray_interactions_df['start'])
        tray_interactions_df['end'] = pd.to_datetime(tray_interactions_df['end'])
        material_interactions_df = pd.DataFrame(material_interactions)
        material_interactions_df['start'] = pd.to_datetime(material_interactions_df['start'])
        material_interactions_df['end'] = pd.to_datetime(material_interactions_df['end'])
        return tray_interactions_df, material_interactions_df
    else:
        raise ValueError('Output format must be \'list\' or \'dataframe\'')

def generate_interaction_data_day(
    target_date,
    time_zone_name,
    environment_id=None,
    environment_name=None,
    start_hour = 8,
    end_hour = 16,
    idle_duration_minutes=20,
    tray_carry_duration_seconds=10,
    material_usage_duration_minutes=40,
    step_size_seconds=0.1,
    interaction_source_type='INFERRED',
    output_format='list',
    write_to_honeycomb=False,
    chunk_size=1000,
    client=None,
    uri=None,
    token_uri=None,
    audience=None,
    client_id=None,
    client_secret=None,
    progress_bar=False,
    notebook=False
):
    # Parse date
    target_date = pd.to_datetime(target_date).date()
    day_start = datetime.datetime(
        target_date.year,
        target_date.month,
        target_date.day,
        start_hour,
        tzinfo=dateutil.tz.gettz(time_zone_name)
    )
    day_end = datetime.datetime(
        target_date.year,
        target_date.month,
        target_date.day,
        end_hour,
        tzinfo=dateutil.tz.gettz(time_zone_name)
    )
    logger.info('Preparing to generate data from {} to {}'.format(
        day_start,
        day_end
    ))
    # Fetch person data
    persons_df = honeycomb_io.fetch_persons(
        person_ids=None,
        person_types=['STUDENT'],
        names=None,
        first_names=None,
        last_names=None,
        nicknames=None,
        short_names=None,
        environment_id=environment_id,
        environment_name=environment_name,
        start=day_start,
        end=day_end,
        output_format='dataframe'
    )
    student_person_ids = persons_df.index.unique().tolist()
    logger.info('Fetched {} students assigned to the specified environment on specified date'.format(
        len(student_person_ids)
    ))
    # Fetch tray and material data
    trays_df = honeycomb_io.fetch_trays(
        tray_ids=None,
        part_numbers=None,
        serial_numbers=None,
        names=None,
        environment_id=environment_id,
        environment_name=environment_name,
        start=day_start,
        end=day_end,
        output_format='dataframe'
    )
    all_tray_ids = trays_df.index.unique().tolist()
    tray_material_assignments_df = honeycomb_io.fetch_tray_material_assignments_by_tray_id(
        tray_ids=all_tray_ids,
        start=day_start,
        end=day_end,
        require_unique_assignment=True,
        require_all_trays=False,
        output_format='dataframe'
    )
    trays_df = trays_df.join(
        tray_material_assignments_df.set_index('tray_id'),
        how='inner'
    )
    tray_ids = trays_df.index.tolist()
    material_ids = trays_df['material_id'].tolist()
    material_id_lookup = {tray_id: material_id for tray_id, material_id in zip(tray_ids, material_ids)}
    logger.info('Fetched {} trays assigned to the specified environment on specified date with materials assigned to them'.format(
        len(material_id_lookup)
    ))
    # Generate data
    tray_interactions, material_interactions = generate_interaction_data_timespan(
        start=day_start,
        end=day_end,
        student_person_ids=student_person_ids,
        material_id_lookup=material_id_lookup,
        idle_duration_minutes=idle_duration_minutes,
        tray_carry_duration_seconds=tray_carry_duration_seconds,
        material_usage_duration_minutes=material_usage_duration_minutes,
        step_size_seconds=step_size_seconds,
        interaction_source_type=interaction_source_type,
        output_format='list',
        progress_bar=progress_bar,
        notebook=notebook
    )
    if write_to_honeycomb:
        tray_interaction_ids = honeycomb_io.create_objects(
            object_name='TrayInteraction',
            data=tray_interactions,
            request_name=None,
            argument_name=None,
            argument_type=None,
            id_field_name=None,
            chunk_size=chunk_size,
            client=client,
            uri=uri,
            token_uri=token_uri,
            audience=audience,
            client_id=client_id,
            client_secret=client_secret
        )
        mterial_interaction_ids = honeycomb_io.create_objects(
            object_name='MaterialInteraction',
            data=material_interactions,
            request_name=None,
            argument_name=None,
            argument_type=None,
            id_field_name=None,
            chunk_size=chunk_size,
            client=client,
            uri=uri,
            token_uri=token_uri,
            audience=audience,
            client_id=client_id,
            client_secret=client_secret
        )
    if output_format == 'list':
        return tray_interactions, material_interactions
    elif output_format == 'dataframe':
        tray_interactions_df = pd.DataFrame(tray_interactions)
        tray_interactions_df['start'] = pd.to_datetime(tray_interactions_df['start'])
        tray_interactions_df['end'] = pd.to_datetime(tray_interactions_df['end'])
        material_interactions_df = pd.DataFrame(material_interactions)
        material_interactions_df['start'] = pd.to_datetime(material_interactions_df['start'])
        material_interactions_df['end'] = pd.to_datetime(material_interactions_df['end'])
        return tray_interactions_df, material_interactions_df
    else:
        raise ValueError('Output format must be \'list\' or \'dataframe\'')

def generate_interaction_data_timespan(
    start,
    end,
    student_person_ids,
    material_id_lookup,
    idle_duration_minutes=20,
    tray_carry_duration_seconds=10,
    material_usage_duration_minutes=40,
    step_size_seconds=0.1,
    interaction_source_type='INFERRED',
    output_format='list',
    progress_bar=False,
    notebook=False
):
    logger.info('Generating data from {} to {}'.format(start, end))
    logger.info('Generating data for {} students'.format(len(student_person_ids)))
    tray_ids = list(material_id_lookup.keys())
    material_ids = list(material_id_lookup.values())
    tray_id_lookup = {material_id: tray_id for tray_id, material_id in material_id_lookup.items()}
    logger.info('Generating data for {} trays/materials'.format(len(tray_ids)))
    # Initial student states
    student_states = dict()
    for student_person_id in student_person_ids:
        student_states[student_person_id] = {
            'state': 'idle',
            'tray_interaction_id': None,
            'material_interation_id': None
        }
    # Initialize tray states
    tray_states = dict()
    for tray_id in tray_ids:
        tray_states[tray_id] = 'on_shelf'
    # Generate data
    num_steps = round((end - start).total_seconds()/step_size_seconds)
    time_series = dict()
    tray_interactions = dict()
    material_interactions = dict()
    if progress_bar:
        if notebook:
            time_step_iterator = tqdm.notebook.tqdm(range(num_steps))
        else:
            time_step_iterator = tqdm.tqdm(range(num_steps))
    else:
        time_step_iterator = range(num_steps)
    for step_index in time_step_iterator:
        timestamp = start + datetime.timedelta(seconds = step_index*step_size_seconds)
        for student_person_id in student_states.keys():
            if student_states[student_person_id]['state'] == 'idle':
                if random.random() > step_size_seconds/(idle_duration_minutes*60):
                    continue
                available_tray_ids = list(filter(
                    lambda tray_id: tray_states[tray_id] == 'on_shelf',
                    tray_states.keys()
                ))
                if len(available_tray_ids) == 0:
                    continue
                selected_tray_id = random.choice(available_tray_ids)
                tray_interaction_id = str(uuid.uuid4())
                tray_interactions[tray_interaction_id] = {
                    'person': student_person_id,
                    'tray': selected_tray_id,
                    'start': honeycomb_io.to_honeycomb_datetime(timestamp),
                    'interaction_type': 'CARRYING_FROM_SHELF',
                    'source_type': interaction_source_type
                }
                student_states[student_person_id]['state'] = 'carrying_from_shelf'
                student_states[student_person_id]['tray_interaction_id'] = tray_interaction_id
                tray_states[selected_tray_id] = 'carrying_from_shelf'
            elif student_states[student_person_id]['state'] == 'carrying_from_shelf':
                if random.random() > step_size_seconds/tray_carry_duration_seconds:
                    continue
                tray_interaction_id = student_states[student_person_id]['tray_interaction_id']
                tray_id = tray_interactions[tray_interaction_id]['tray']
                material_id = material_id_lookup[tray_id]
                material_interaction_id = str(uuid.uuid4())
                material_interactions[material_interaction_id] = {
                    'person': student_person_id,
                    'material': material_id,
                    'start': honeycomb_io.to_honeycomb_datetime(timestamp),
                    'source_type': interaction_source_type
                }
                tray_interactions[tray_interaction_id]['end'] = honeycomb_io.to_honeycomb_datetime(timestamp)
                student_states[student_person_id]['state'] = 'using_material'
                student_states[student_person_id]['tray_interaction_id'] = None
                student_states[student_person_id]['material_interaction_id'] = material_interaction_id
                tray_states[tray_id] = 'using_material'
            elif student_states[student_person_id]['state'] == 'using_material':
                if random.random() > step_size_seconds/(material_usage_duration_minutes*60):
                    continue
                material_interaction_id = student_states[student_person_id]['material_interaction_id']
                material_id = material_interactions[material_interaction_id]['material']
                tray_id = tray_id_lookup[material_id]
                tray_interaction_id = str(uuid.uuid4())
                tray_interactions[tray_interaction_id] = {
                    'person': student_person_id,
                    'tray': tray_id,
                    'start': honeycomb_io.to_honeycomb_datetime(timestamp),
                    'interaction_type': 'CARRYING_TO_SHELF',
                    'source_type': interaction_source_type
                }
                material_interactions[material_interaction_id]['end'] = honeycomb_io.to_honeycomb_datetime(timestamp)
                student_states[student_person_id]['state'] = 'carrying_to_shelf'
                student_states[student_person_id]['tray_interaction_id'] = tray_interaction_id
                student_states[student_person_id]['material_interaction_id'] = None
                tray_states[tray_id] = 'carrying_to_shelf'
            elif student_states[student_person_id]['state'] == 'carrying_to_shelf':
                if random.random() > step_size_seconds/tray_carry_duration_seconds:
                    continue
                tray_interaction_id = student_states[student_person_id]['tray_interaction_id']
                tray_id = tray_interactions[tray_interaction_id]['tray']
                tray_interactions[tray_interaction_id]['end'] = honeycomb_io.to_honeycomb_datetime(timestamp)
                student_states[student_person_id]['state'] = 'idle'
                student_states[student_person_id]['tray_interaction_id'] = None
                tray_states[tray_id] = 'on_shelf'
            else:
                raise ValueError('Student state \'{}\' not recognized'.format(
                    student_states[student_person_id]['state']
                ))
    if output_format == 'list':
        return list(tray_interactions.values()), list(material_interactions.values())
    elif output_format == 'dataframe':
        tray_interactions_df = pd.DataFrame(tray_interactions.values())
        tray_interactions_df['start'] = pd.to_datetime(tray_interactions_df['start'])
        tray_interactions_df['end'] = pd.to_datetime(tray_interactions_df['end'])
        material_interactions_df = pd.DataFrame(material_interactions.values())
        material_interactions_df['start'] = pd.to_datetime(material_interactions_df['start'])
        material_interactions_df['end'] = pd.to_datetime(material_interactions_df['end'])
        return tray_interactions_df, material_interactions_df
    else:
        raise ValueError('Output format must be \'list\' or \'dataframe\'')
